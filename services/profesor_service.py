from models.profesor import crear_profesor, obtener_profesores
from utils.exceptions import APIError

def registrar_profesor(data):
    nombre = data.get("nombre")
    apellido = data.get("apellido")

    if not all([nombre, apellido]):
        raise APIError ("Faltan datos", 400)

    crear_profesor(nombre, apellido)
    raise APIError ("Profesor creado correctamente", 201)


def listar_profesores():
    return obtener_profesores(), 200