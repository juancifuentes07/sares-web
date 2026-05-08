import re
import sqlite3
from models.estudiante import crear_estudiante, obtener_estudiantes
from models.estudiante import obtener_estudiante_por_id
from utils.exceptions import APIError
from werkzeug.security import generate_password_hash

def registrar_estudiante(data):
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    documento = data.get("documento")
    carrera = data.get("carrera")
    password = data.get("password")

    if not all([nombre, apellido, documento, carrera, password]):
        return {"error": "Faltan datos"}, 400 

    nombre = nombre.strip().title()
    apellido = apellido.strip().title()
    documento = documento.strip()
    carrera = carrera.strip().title()

    # Validar formato del documento
    if not re.match(r"^\d{1,10}$", documento):
        return {"error": "Formato de documento inválido"}, 400
    
    if len(password) < 6:
        return {"error": "La contraseña debe tener al menos 6 caracteres"}, 400
    
    password_hash = generate_password_hash(password)

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