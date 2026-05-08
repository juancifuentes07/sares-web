import re
import sqlite3
from models.estudiante import crear_estudiante, obtener_estudiantes
from models.estudiante import obtener_estudiante_por_id
from utils.exceptions import APIError

def registrar_estudiante(data):
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    documento = data.get("documento")
    carrera = data.get("carrera")

    if not all([nombre, apellido, documento, carrera]):
        return {"error": "Faltan datos"}, 400
    
    nombre = nombre.strip().title()
    apellido = apellido.strip().title()
    documento = documento.strip()
    carrera = carrera.strip().title()

    # Validar formato del documento
    if not re.match(r"^\d{1,10}$", documento):
        return {"error": "Formato de documento inválido"}, 400

    try:
        crear_estudiante(nombre, apellido, documento, carrera)
        return {"mensaje": "Estudiante creado correctamente"}, 201

    except sqlite3.IntegrityError:
        return {"error": "El documento ya existe"}, 400


def listar_estudiantes():
    return obtener_estudiantes(), 200


def obtener_estudiante(id):
    estudiante = obtener_estudiante_por_id(id)

    if estudiante:
        return estudiante, 200
    return {"error": "Estudiante no encontrado"}, 404

from models.estudiante import eliminar_estudiante

def borrar_estudiante(id):
    cambios = eliminar_estudiante(id)

    if cambios == 0:
        return {"error": "Estudiante no encontrado"}, 404

    return {"mensaje": "Estudiante eliminado correctamente"}, 200