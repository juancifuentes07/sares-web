<<<<<<< HEAD
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
=======
import oracledb
from config import Config

def get_connection():
    # Usa la configuración que guardaste en config.py
    return oracledb.connect(
        user=Config.USUARIO,
        password=Config.PASSWORD,
        dsn=f"{Config.HOST}:{Config.PUERTO}/{Config.SERVICIO}"
    )

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Aquí es donde fallaba: Oracle no usa 'executescript' de la misma forma que SQLite
    with open('database/schema.sql', 'r', encoding='utf-8') as f:
        sql_commands = f.read().split(';')
        for command in sql_commands:
            if command.strip():
                cursor.execute(command)
    conn.commit()
    cursor.close()
    conn.close()
>>>>>>> origin/master
