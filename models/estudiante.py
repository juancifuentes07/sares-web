from database.init_db import get_connection

def crear_estudiante(nombre, apellido, documento, carrera, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO estudiantes (nombre, apellido, documento, carrera, password_hash)
            VALUES (:nombre, :apellido, :documento, :carrera, :password_hash)
        """, {
            "nombre": nombre,
            "apellido": apellido,
            "documento": documento,
            "carrera": carrera,
            "password_hash": password_hash
        })
        conn.commit()

        cursor.execute(
            "SELECT id, nombre, apellido, documento, carrera FROM estudiantes WHERE documento = :documento",
            {"documento": documento}
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "nombre": row[1],
                "apellido": row[2],
                "documento": row[3],
                "carrera": row[4]
            }
        return None
    finally:
        cursor.close()
        conn.close()

def obtener_estudiantes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, apellido, documento, carrera FROM estudiantes")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": r[0], "nombre": r[1], "apellido": r[2], "documento": r[3], "carrera": r[4]} for r in rows]

def obtener_estudiante_por_id(estudiante_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, apellido, documento, carrera FROM estudiantes WHERE id = :id", {"id": estudiante_id})
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return {"id": row[0], "nombre": row[1], "apellido": row[2], "documento": row[3], "carrera": row[4]}
    return None

def obtener_estudiante_por_documento(documento):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre, apellido, documento, carrera, password_hash
        FROM estudiantes WHERE documento = :doc
    """, {"doc": documento})
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return {"id": row[0], "nombre": row[1], "apellido": row[2], "documento": row[3], "carrera": row[4], "password_hash": row[5]}
    return None

def eliminar_estudiante(estudiante_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM estudiantes WHERE id = :id", {"id": estudiante_id})
    conn.commit()
    cambios = cursor.rowcount
    cursor.close()
    conn.close()
    return cambios