import oracledb
# Importamos con alias para evitar conflictos con los nombres de las funciones locales
from models.profesor import crear_profesor as db_crear_profesor, obtener_profesores as db_obtener_profesores
from utils.exceptions import APIError

def registrar_profesor(data):
    """
    Valida los datos y registra un nuevo profesor en la base de datos Oracle.
    """
    nombre = data.get("nombre")
    apellido = data.get("apellido")

    # Validación de campos obligatorios
    if not all([nombre, apellido]):
        return {"error": "Faltan datos obligatorios (nombre y apellido)"}, 400

    # Limpieza de datos (Quitar espacios y poner formato Título)
    nombre = nombre.strip().title()
    apellido = apellido.strip().title()

    try:
        # Llamada al modelo que ya configuramos con :nombre y :apellido para Oracle
        db_crear_profesor(nombre, apellido)
        return {"mensaje": f"Profesor {nombre} {apellido} creado correctamente en Oracle"}, 201
    except oracledb.Error as e:
        # Captura errores específicos de Oracle (conexión, permisos del usuario system, etc.)
        return {"error": f"Error en la base de datos Oracle: {str(e)}"}, 500


def listar_profesores():
    """
    Recupera el listado de todos los profesores desde el servicio 'xe'.
    """
    try:
        profesores = db_obtener_profesores()
        return profesores, 200
    except Exception as e:
        return {"error": f"No se pudo obtener la lista de profesores: {str(e)}"}, 500