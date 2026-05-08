from werkzeug.security import check_password_hash
from models.estudiante import obtener_estudiante_por_documento

def login_estudiante(documento, password):
    estudiante = obtener_estudiante_por_documento(documento)

    if not estudiante:
        return None, "Documento no registrado"

    if not check_password_hash(estudiante["password_hash"], password):
        return None, "Contraseña incorrecta"

    return estudiante, None