from pic_to_xlsx import pic_to_xlsx
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from xlsx_to_db import xlsx_to_db
import db
import aiapi

root = Tk()
root.withdraw()
pic_path = askopenfilename(initialdir=os.path.dirname(__file__), title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp")])
root.destroy()
if not pic_path:
    print("No file selected. Exiting...")
    exit()
print("Pic path:", pic_path)

def preprocess():
    print("Starting pic to xlsx...")
    xlsx_path = pic_to_xlsx(pic_path)
    # xlsx_path = 'output/xlsx/0194cc08-946f-4cfd-acee-4baec579fda9.xlsx'
    print("Pic to xlsx finished. XLSX file:", xlsx_path)

    print("Starting xlsx to db...")
    db_path = xlsx_to_db(xlsx_path)
    # db_path = 'output/db/0194cc08-946f-4cfd-acee-4baec579fda9.db'
    print("Xlsx to db finished. DB file:", db_path)
    return db_path

def interactive(db_path):
    conn = db.open_db(db_path)
    print("Interactive mode started. Type 'exit' to exit. Target Pic:", pic_path)
    while True:
        query = input("\nchat_with_pic> ")
        if query.lower() == "exit":
            break
        info = db.query_info(conn)
        commands = aiapi.process_query(query, info)
        commands_res = db.execute_commands(conn, commands)
        aiapi.query_final(query, info, commands_res)
        
db_path = preprocess()
# db_path = 'output/db/4d9e4ec7-daf8-4849-b60d-8871f20f9e81.db'
print("All processes finished. Start interactive mode.")
interactive(db_path)