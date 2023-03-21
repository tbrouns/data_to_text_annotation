import argparse
import glob
import os
import sqlite3

import pandas as pd

from py_utils.utils_data import save_pickle
from py_utils.utils_general import get_basename_no_ext

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--db_dir", required=True, help="Path to directory containing one or more db files")
args = parser.parse_args()

# Get the db files
data_dir = args.db_dir
db_file_list = glob.glob(os.path.join(data_dir, "*.db"))

# Initialize dict
data_dict = {"summary": [], "filepath": []}

# Loop through all the db files
for db_file_path in db_file_list:

    # Create the sql connection
    conn = sqlite3.connect(db_file_path)

    # Get the full dataframe
    df = pd.read_sql_query("SELECT * from data_table", conn)

    # Run through all the data in the database
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

# Save the combined data in PKL file
save_pickle(os.path.join(data_dir, "data.pkl"), data_dict)
