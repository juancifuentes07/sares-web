import oracledb
# Importamos las funciones que ya migramos a Oracle en el modelo
from models.materia import crear_materia as db_crear_materia, obtener_materias as db_obtener_materias
from utils.exceptions import APIError

def registrar_materia(data):
    """
    Valida y registra una nueva materia en la base de datos Oracle.
    """
    nombre = data.get("nombre")
    carrera = data.get("carrera")

    if not all([nombre, carrera]):
        # Usamos la excepción personalizada que ya tienes definida
        raise APIError("Faltan datos obligatorios (nombre y carrera)", 400)

    # Limpieza básica de datos antes de insertar en Oracle
    nombre = nombre.strip().title()
    carrera = carrera.strip().title()

    try:
        db_crear_materia(nombre, carrera)
        return {"mensaje": f"Materia '{nombre}' registrada correctamente en Oracle"}, 201
    except oracledb.Error as e:
        return {"error": f"Error técnico en Oracle: {str(e)}"}, 500

def listar_materias():
    """
    Obtiene el listado completo de materias desde el servicio 'xe'.
    """
    try:
        # Esta llamada ahora va directo a tu usuario 'system' en Oracle
        materias = db_obtener_materias()
        return materias, 200
    except Exception as e:
        return {"error": f"No se pudieron cargar las materias: {str(e)}"}, 500