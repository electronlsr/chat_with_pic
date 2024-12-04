import sqlite3
import configparser
import os

config = configparser.ConfigParser()
config.read("config.conf")

def open_db(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def query_info(conn):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info(data);")
    columns = cursor.fetchall()
    fields = [f"{col[1]}: {col[2]}" for col in columns]
    fields_str = ", ".join(fields)
    cursor.execute(f"SELECT * FROM data LIMIT 2;")
    rows = cursor.fetchall()
    data_lines = []
    for row in rows:
        row_str = ", ".join(str(item) for item in row)
        data_lines.append(row_str)
    data_str = "\n".join(data_lines)
    return f"结构：{fields_str}\n前两条数据：{data_str}"

def execute_commands(conn, commands):
    res = ""
    cursor = conn.cursor()
    for command in commands:
        now = cursor.execute(command)
        res = res + command + " : " + str(now.fetchall()) + "\n"
    conn.commit()
    return res