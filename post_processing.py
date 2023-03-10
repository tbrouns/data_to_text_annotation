import glob
import os
import sqlite3

import pandas as pd

from py_utils.utils_data import save_pickle
from py_utils.utils_general import get_basename_no_ext

# create a connection to the database

data_dir = "/home/tsn/Projects/buienradar/weather_data/dataset/"
db_file_list = glob.glob(os.path.join(data_dir, "*.db"))

data_dict = {"summary": [], "filepath": []}

for db_file_path in db_file_list:
    conn = sqlite3.connect(db_file_path)

    df = pd.read_sql_query("SELECT * from data_table", conn)

    database_name = get_basename_no_ext(db_file_path)
    for filename, text in zip(df["filename"], df["text"]):
        csv_path = os.path.join(data_dir, database_name, filename)
        if os.path.isfile(csv_path):
            data_dict["filepath"].append(csv_path)
            data_dict["summary"].append(text)
        else:
            print(f"{csv_path} not found!")

    # close the connection
    conn.close()

save_pickle(os.path.join(data_dir, "train.pkl"), data_dict)