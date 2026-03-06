import sqlite3

DB_NAME = "sares.db"

def crear_profesor(nombre, apellido):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO profesores (nombre, apellido)
        VALUES (?, ?)
    """, (nombre, apellido))

    conn.commit()
    conn.close()


def obtener_profesores():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profesores")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]