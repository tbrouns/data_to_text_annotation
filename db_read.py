import sqlite3
import pandas as pd

# create a connection to the database
conn = sqlite3.connect("data.db")

df = pd.read_sql_query("SELECT * from data_table", conn)
print(df)

# close the connection
conn.close()
