import sqlite3

DB_NAME = "sares.db"

def crear_materia(nombre, profesor_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO materias (nombre, profesor_id)
        VALUES (?, ?)
    """, (nombre, profesor_id))

    conn.commit()
    conn.close()


def obtener_materias():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, carrera, semestre
        FROM materias
        ORDER BY semestre
    """)
    
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]