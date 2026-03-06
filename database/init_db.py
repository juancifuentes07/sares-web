import sqlite3

def init_db():
    print("Inicializando base de datos...")

    conn = sqlite3.connect("sares.db")

    with open("database/schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.close()

def get_connection():
    conn = sqlite3.connect("sares.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn