import sqlite3
from models.inscripcion import crear_inscripcion, obtener_inscripciones
from database.init_db import get_connection
from utils.exceptions import APIError

def registrar_inscripcion(data):
    estudiante_id = data.get("estudiante_id")
    materia_id = data.get("materia_id")

    if not all([estudiante_id, materia_id]):
        return {"error": "Faltan datos"}, 400

    conn = get_connection()
    cursor = conn.cursor()

    # 🔎 Verificar que el estudiante exista
    cursor.execute("SELECT id FROM estudiantes WHERE id = ?", (estudiante_id,))
    if not cursor.fetchone():
        conn.close()
        return {"error": "El estudiante no existe"}, 404

    # 🔎 Verificar que la materia exista
    cursor.execute("SELECT id FROM materias WHERE id = ?", (materia_id,))
    if not cursor.fetchone():
        conn.close()
        return {"error": "La materia no existe"}, 404

    # 🔎 Verificar que no esté duplicada
    cursor.execute("""
        SELECT id FROM inscripciones 
        WHERE estudiante_id = ? AND materia_id = ?
    """, (estudiante_id, materia_id))

    if cursor.fetchone():
        conn.close()
        return {"error": "El estudiante ya está inscrito en esta materia"}, 400

    # ✅ Insertar
    cursor.execute("""
        INSERT INTO inscripciones (estudiante_id, materia_id)
        VALUES (?, ?)
    """, (estudiante_id, materia_id))

    conn.commit()
    conn.close()

    return {"mensaje": "Inscripción realizada correctamente"}, 201

def listar_inscripciones():
    return obtener_inscripciones(), 200

def actualizar_notas(inscripcion_id, data):
    nota1 = data.get("nota_corte1")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE inscripciones
        SET nota_corte1 = ?
        WHERE id = ?
    """, (nota1, inscripcion_id))

    if cursor.rowcount == 0:
        conn.close()
        return {"error": "Inscripción no encontrada"}, 404

    conn.commit()
    conn.close()

    return {"mensaje": "Notas actualizadas correctamente"}, 200