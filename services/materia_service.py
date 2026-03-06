import sqlite3
from models.materia import crear_materia, obtener_materias
from utils.exceptions import APIError
from database.init_db import init_db


def registrar_materia(estudiante_id, carrera, materia, semestre):

    conn = init_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO materias (estudiante_id, carrera, materia, semestre)
    VALUES (?, ?, ?, ?)
    """

    cursor.execute(query, (estudiante_id, carrera, materia, semestre))

    conn.commit()
    conn.close()

    return {"mensaje": "Materia registrada correctamente"}, 201


def listar_materias():
    return obtener_materias(), 200