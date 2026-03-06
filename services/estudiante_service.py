from models.estudiante import crear_estudiante, obtener_estudiantes
from models.estudiante import obtener_estudiante_por_id
from utils.exceptions import APIError

import sqlite3

def registrar_estudiante(data):
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    documento = data.get("documento")
    carrera = data.get("carrera")
    semestre = data.get("semestre")

    if not all([nombre, apellido, documento, carrera, semestre]):
        raise APIError ("Faltan datos", 400)

    try:
        crear_estudiante(nombre, apellido, documento, carrera, semestre)
        raise APIError ("Estudiante creado correctamente", 201)

    except sqlite3.IntegrityError:
        raise APIError ("El documento ya existe", 400)


def listar_estudiantes():
    return obtener_estudiantes(), 200


def obtener_estudiante(id):
    estudiante = obtener_estudiante_por_id(id)

    if estudiante:
        return estudiante, 200
    raise APIError ("Estudiante no encontrado", 404)

from models.estudiante import eliminar_estudiante

def borrar_estudiante(id):
    cambios = eliminar_estudiante(id)

    if cambios == 0:
        raise APIError ("Estudiante no encontrado", 404)

    raise APIError ("Estudiante eliminado correctamente", 200)