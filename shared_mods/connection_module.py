import sqlite3

""" create a database connection to a SQLite database """

conn = None
try:

    # conn = sqlite3.connect('../' + 'database.db')
    conn = sqlite3.connect('database.db')
except sqlite3.Error as e:
    print(e)

cur = conn.cursor()