import pandas as pd
import configparser
import os
from aiapi import process_csv
import db

config = configparser.ConfigParser()
config.read("config.conf")

def xlsx_to_csv(xlsx_path):
    data = pd.read_excel(xlsx_path)
    csv_path = config['Directory']['csv_dir'] + "/" + os.path.splitext(os.path.basename(xlsx_path))[0] + ".csv"
    data.to_csv(csv_path, index=False, header=False, encoding='utf-8')
    return csv_path

def csv_to_db(csv_path):
    db_path = config['Directory']['db_dir'] + "/" + os.path.splitext(os.path.basename(csv_path))[0] + ".db"
    conn = db.open_db(db_path)
    data = pd.read_csv(csv_path)
    data.to_sql("data", conn, if_exists="replace", index=False)
    conn.close()
    return db_path

def xlsx_to_db(xlsx_path):
    print("Starting xlsx to csv...")
    csv_path = xlsx_to_csv(xlsx_path)
    # csv_path = 'output/csv/0194cc08-946f-4cfd-acee-4baec579fda9.csv'
    print("XlSX to csv finished. CSV file:", csv_path)
    print("Starting pre-processing...")
    process_csv(csv_path)
    print("Pre-processing finished.")
    return csv_to_db(csv_path)
    