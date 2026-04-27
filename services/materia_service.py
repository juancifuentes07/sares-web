import sqlite3
from models.materia import crear_materia, obtener_materias
from utils.exceptions import APIError
from database.init_db import init_db


def registrar_materia(data):

    nombre = data.get("nombre")
    carrera = data.get("carrera")

    if not all([nombre, carrera]):
        raise APIError({"error": "Faltan datos"}, 400)

    crear_materia(nombre, carrera)
    return {"mensaje": "Materia registrada correctamente"}, 201

def listar_materias():
    return obtener_materias(), 200