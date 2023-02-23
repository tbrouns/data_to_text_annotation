import sqlite3

# create a connection to the database
conn = sqlite3.connect("data.db")

# create a cursor object to execute SQL commands
cursor = conn.cursor()

# create a table in the database
cursor.execute(
    """DROP TABLE IF EXISTS weather_data"""
)
cursor.execute(
    """CREATE TABLE weather_data
                  (id INTEGER,
                   data TEXT NOT NULL,
                    UNIQUE (id) ON CONFLICT REPLACE)"""
)

# commit the changes to the database
conn.commit()

# close the connection
conn.close()
