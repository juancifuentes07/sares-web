import re
import oracledb
from werkzeug.security import generate_password_hash
from models.estudiante import crear_estudiante, obtener_estudiantes, obtener_estudiante_por_id, eliminar_estudiante

def validar_password(password):
    if len(password) < 8:
        return "La contraseña debe tener al menos 8 caracteres"
    if not re.search(r"[A-Z]", password):
        return "La contraseña debe contener al menos una letra mayúscula"
    if not re.search(r"[a-z]", password):
        return "La contraseña debe contener al menos una letra minúscula"
    if not re.search(r"\d", password):
        return "La contraseña debe contener al menos un número"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "La contraseña debe contener al menos un carácter especial"
    return None

def registrar_estudiante(data):
    nombre    = data.get("nombre")
    apellido  = data.get("apellido")
    documento = data.get("documento")
    carrera   = data.get("carrera")
    password  = data.get("password")

    if not all([nombre, apellido, documento, carrera, password]):
        return {"error": "Faltan datos"}, 400

    nombre    = nombre.strip().title()
    apellido  = apellido.strip().title()
    documento = documento.strip()
    carrera   = carrera.strip().title()

    if not re.match(r"^\d{1,10}$", documento):
        return {"error": "Formato de documento inváli|do"}, 400

    error_password = validar_password(password)
    if error_password:
        return {"error": error_password}, 400

    password_hash = generate_password_hash(password)

    try:
        crear_estudiante(nombre, apellido, documento, carrera, password_hash)
        return {"mensaje": "Estudiante creado correctamente"}, 201
    except oracledb.IntegrityError:
        return {"error": "El documento ya existe"}, 400
    except oracledb.Error as e:
        return {"error": f"Error en la base de datos: {str(e)}"}, 500

def listar_estudiantes():
    return obtener_estudiantes(), 200

def obtener_estudiante(id):
    estudiante = obtener_estudiante_por_id(id)
    if estudiante:
        return estudiante, 200
    return {"error": "Estudiante no encontrado"}, 404

def borrar_estudiante(id):
    cambios = eliminar_estudiante(id)
    if cambios == 0:
        return {"error": "Estudiante no encontrado"}, 404
    return {"mensaje": "Estudiante eliminado correctamente"}, 200