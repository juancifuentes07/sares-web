import sqlite3

DB_NAME = "sares.db"

def crear_estudiante(nombre, apellido, documento, carrera):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO estudiantes (nombre, apellido, documento, carrera)
        VALUES (?, ?, ?, ?)
    """, (nombre, apellido, documento, carrera))

    conn.commit()
    conn.close()


def obtener_estudiantes():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM estudiantes")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

def obtener_estudiante_por_id(estudiante_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM estudiantes WHERE id = ?", (estudiante_id,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)
    return None

def eliminar_estudiante(estudiante_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM estudiantes WHERE id = ?", (estudiante_id,))
    
    conn.commit()
    cambios = cursor.rowcount
    conn.close()

    return cambios