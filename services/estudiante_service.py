import re
import oracledb  # Cambiamos sqlite3 por el driver de Oracle
from models.estudiante import (
    crear_estudiante, 
    obtener_estudiantes, 
    obtener_estudiante_por_id, 
    eliminar_estudiante
)
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

    # Validar formato del documento (máximo 10 dígitos)
    if not re.match(r"^\d{1,10}$", documento):
        return {"error": "Formato de documento inválido"}, 400

    try:
        crear_estudiante(nombre, apellido, documento, carrera)
        return {"mensaje": "Estudiante creado correctamente"}, 201

    except oracledb.IntegrityError:
        # Oracle lanza IntegrityError cuando se viola una restricción UNIQUE o PRIMARY KEY
        return {"error": "El documento ya existe en la base de datos de Oracle"}, 400
    except oracledb.Error as e:
        # Captura otros errores específicos de Oracle (ej. conexión, permisos)
        return {"error": f"Error en la base de datos: {str(e)}"}, 500


def listar_estudiantes():
    # Esta función ahora traerá los datos desde tu servicio 'xe'
    return obtener_estudiantes(), 200


def obtener_estudiante(id):
    estudiante = obtener_estudiante_por_id(id)
    if estudiante:
        return estudiante, 200
    return {"error": "Estudiante no encontrado"}, 404


def borrar_estudiante(id):
    # Asegúrate de que eliminar_estudiante en models/estudiante.py use :id
    cambios = eliminar_estudiante(id)

    if cambios == 0:
        return {"error": "Estudiante no encontrado"}, 404

    return {"mensaje": "Estudiante eliminado correctamente"}, 200