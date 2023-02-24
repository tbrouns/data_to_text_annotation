import os
import sqlite3

import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="template")

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create data
CURRENT_FRAME = 0
DATA_FRAMES = []
for i in range(0, 3):
    data = {"numbers": [i + 1, i + 2, i + 3], "text": ["hi", "hello", "goodbye"]}
    df = pd.DataFrame(data)
    DATA_FRAMES.append(df)

@app.route("/")
def index():
    global CURRENT_FRAME
    return render_template(
        "index.html", data_frames=DATA_FRAMES, current_frame=CURRENT_FRAME
    )


@app.route("/submit", methods=["POST"])
def submit():
    global CURRENT_FRAME
    if request.method == "POST":
        filename = os.path.basename(CSV_FILES[CURRENT_FRAME])
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO data_table (id, filename, text) VALUES (?, ?)",
            (CURRENT_FRAME, filename, [request.form["text"]),
        )
        conn.commit()
        conn.close()
        CURRENT_FRAME += 1
    max_index = len(DATA_FRAMES) - 1
    if CURRENT_FRAME > max_index:
        CURRENT_FRAME = max_index
    return index()

