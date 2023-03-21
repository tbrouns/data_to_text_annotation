import argparse
import glob
import os
import sqlite3

import pandas as pd
from flask import Flask, render_template, request

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--csv_dir", required=True, help="Path to directory containing one or more CSV files")
args = parser.parse_args()

# Set-up Flask app
app = Flask(__name__, template_folder="template")

# Get the data
CSV_FILES = sorted(
    glob.glob(os.path.join(args.csv_dir, "*.csv"))
)

# Constants
CURRENT_FRAME = 0


def check_if_exists(filename):
    """Check if the filename already exists in the database

    :param filename: name of the CSV file
    :return: True if the filename exists in database
    """
    conn = sqlite3.connect("data.db")
    # Get dataframe from the database
    df = pd.read_sql_query("SELECT * from data_table", conn)
    # Check if file exists
    if filename in df["filename"].values:
        entry_exists = True
    else:
        entry_exists = False
    # Close the connection
    conn.close()
    return entry_exists


@app.route("/")
def index():
    """Render the HTML page

    :return:
    """
    global CURRENT_FRAME
    entry_exists = True
    # Get a CSV file that doesn't exist in the database
    while entry_exists:
        filepath = CSV_FILES[CURRENT_FRAME]
        filename = os.path.basename(filepath)
        entry_exists = check_if_exists(filename)
        if entry_exists:
            # Go to the next file if this one exists
            CURRENT_FRAME += 1
        # Stop checking once we reach the end
        max_index = len(CSV_FILES) - 1
        if CURRENT_FRAME > max_index:
            break
    # Read the CSV data
    df = pd.read_csv(filepath)
    # Use the basename as the index name for additional metadata
    df.index.name = os.path.basename(filepath)
    # Convert the dataframe to html
    pd.set_option("display.max_colwidth", 1)
    html = df.to_html()
    return render_template("index.html", data_frame=html)


@app.route("/submit", methods=["POST"])
def submit():
    global CURRENT_FRAME
    if request.method == "POST":
        filename = os.path.basename(CSV_FILES[CURRENT_FRAME])
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO data_table (id, filename, text) VALUES (?, ?, ?)",
            (CURRENT_FRAME, filename, request.form["text"]),
        )
        conn.commit()
        conn.close()
        CURRENT_FRAME += 1
    max_index = len(CSV_FILES) - 1
    if CURRENT_FRAME > max_index:
        CURRENT_FRAME = max_index
    return index()


if __name__ == "__main__":
    app.run()
