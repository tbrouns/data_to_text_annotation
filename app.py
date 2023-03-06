import glob
import os
import sqlite3

import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="template")

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create data
CSV_FILES = sorted(
    glob.glob("/home/tsn/Projects/buienradar/weather_data/csv_batch_03_05/*.csv")
)
CURRENT_FRAME = 0


def check_if_exists(filename):
    conn = sqlite3.connect("data.db")
    df = pd.read_sql_query("SELECT * from data_table", conn)
    entry_exists = False
    if filename in df["filename"].values:
        entry_exists = True
    # close the connection
    conn.close()
    return entry_exists


@app.route("/")
def index():
    global CURRENT_FRAME
    entry_exists = True
    while entry_exists:
        filepath = CSV_FILES[CURRENT_FRAME]
        filename = os.path.basename(filepath)
        entry_exists = check_if_exists(filename)
        if entry_exists:
            CURRENT_FRAME += 1
        max_index = len(CSV_FILES) - 1
        if CURRENT_FRAME > max_index:
            break
    city_name = os.path.basename(filepath).split("_")[0]
    df = pd.read_csv(filepath)
    df.index.name = city_name
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
