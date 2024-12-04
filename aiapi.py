from openai import OpenAI
import configparser

config = configparser.ConfigParser()
config.read("config.conf")

client = OpenAI(
    api_key = config['Model']['api_key'],
    base_url = config['Model']['base_url']
)

def process_csv(csv_path):
    with open(csv_path, "r", encoding='utf-8') as file:
        data = file.read()
    completion = client.chat.completions.create(
        model = config['Model']['transfer_model'],
        messages = [
            {"role": "system", "content": "接下来我将给出一个csv文件的内容，它基于图片识别而来，请你将其中的信息整理好方便我将其转换为数据库。具体要求：1. 每一列都有具体含义，其中某些列可能已经给出标题，如果没有给出标题请你完善第一行以注明每一列的标题，这在之后会被转换为数据库的字段名 2. 无用的、不知道意义的数据可以删除 3. 如果某一列的数据的类型不同（比如同时出现了 90 和 优秀），请务必确保你根据自己的理解将其全都转换成同一种数据类型，以便我直接存入数据库后续调取使用 4. 你只需要返回整理后的 csv 的内容，不可以返回其他任何东西，也不要附带任何格式。以下是内容："},
            {"role": "user", "content": data}
        ]
    )
    with open(csv_path, "w", encoding='utf-8') as file:
        file.write(completion.choices[0].message.content.replace("```", "").replace("csv", "").strip())

def process_query(query, info):
    completion = client.chat.completions.create(
        model = config['Model']['query_model'],
        messages= [
            {"role": "system", "content": f"接下来我需要通过获取一个sqlite3数据库的部分信息以解决一些问题，其中只有一张数据表data。我将给出该数据库的结构以及前两条数据的内容，接下来我会问若干个问题，请你针对每个问题，给出为了解决这个问题所需要的数据库查询语句。请注意，除了查询语句外不要回复任何其他内容，也不需要回复任何格式，如果需要多个语句换行即可，同一条语句只可以出现在同一行！\n{info}\n以下是问题："},
            {"role": "user", "content": query}
        ]
    )
    return completion.choices[0].message.content.splitlines()

def query_final(query, info, commands_res):
    completion = client.chat.completions.create(
        model = config['Model']['query_model'],
        messages= [
            {"role": "system", "content": f"请你根据一个sqlite3数据库的结构，一些查询语句和查询结果回答问题。你的回答应当尽可能客观且详尽，所使用的数据必须是查询结果中提到的数据。\n该数据库的结构：{info}"},
            {"role": "user", "content": f"查询语句及结果：{commands_res}\n问题：{query}"}
        ],
        stream=True,
    )
    for message in completion:
        print(message.choices[0].delta.content, end="")