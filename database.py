import sqlite3

def get_connection():
    conn = sqlite3.connect("mydata.db")  # this creates the file if it doesn't exist
    return conn
