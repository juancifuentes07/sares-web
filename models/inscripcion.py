import sqlite3

DB_NAME = "sares.db"

def crear_inscripcion(estudiante_id, materia_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO inscripciones (estudiante_id, materia_id)
        VALUES (?, ?)
    """, (estudiante_id, materia_id))

    conn.commit()
    conn.close()


def obtener_inscripciones():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            i.id,
            e.nombre || ' ' || e.apellido AS estudiante,
            m.nombre AS materia,
            i.nota_corte1
        FROM inscripciones i
        JOIN estudiantes e ON i.estudiante_id = e.id
        JOIN materias m ON i.materia_id = m.id
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]