import sqlite3

DB_NAME = "sares.db"

def crear_materia(nombre, carrera):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO materias (nombre, carrera)
        VALUES (?, ?)
    """, (nombre, carrera))
    conn.commit()
    conn.close()

def obtener_materias():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, carrera
        FROM materias
    """)
    
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]