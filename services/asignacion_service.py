"""
Servicio de asignación automática de profesores de apoyo.

Cuando un estudiante registra una nota que lo deja "en riesgo" en una
materia, este servicio le asigna automáticamente un profesor EXPERTO en
esa materia, elegido de forma ALEATORIA entre los disponibles.
"""

import random

from database.init_db import get_connection
from models.profesor import obtener_profesores_de_materia
from models.seguimiento import existe_seguimiento, crear_seguimiento
from models.tarea import crear_tarea

# Nota mínima para aprobar. Si la nota del corte está por debajo, hay riesgo.
NOTA_APROBATORIA = 3.0

# Actividades que se asignan al estudiante al iniciarse el seguimiento.
# El profesor puede editarlas o agregar más desde su panel.
TAREAS_INICIALES = [
    "Realizar el taller de refuerzo de los temas del primer corte",
    "Repasar los temas reprobados y traer dudas a la próxima tutoría",
    "Asistir a la primera sesión de acompañamiento con el profesor",
]


def esta_en_riesgo(nota_corte1):
    """Determina si una nota deja al estudiante en riesgo de perder la materia.

    Criterio: la nota del primer corte está por debajo de la nota aprobatoria.
    """
    if nota_corte1 is None or nota_corte1 <= 0:
        return False  # Sin nota registrada: no se evalúa todavía.
    return float(nota_corte1) < NOTA_APROBATORIA


def _obtener_inscripcion(inscripcion_id):
    """Consulta una inscripción con su materia. Devuelve dict o None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id, i.materia_id, i.nota_corte1, m.nombre
        FROM inscripciones i
        JOIN materias m ON i.materia_id = m.id
        WHERE i.id = :id
    """, {"id": inscripcion_id})
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return {"id": row[0], "materia_id": row[1],
                "nota_corte1": row[2], "materia_nombre": row[3]}
    return None


def evaluar_y_asignar(inscripcion_id):
    """Revisa una inscripción y, si el estudiante está en riesgo, le asigna
    automáticamente un profesor experto de la materia, elegido al azar.

    Es seguro llamarla siempre que se actualice una nota: si no hay riesgo
    o ya hay seguimiento, simplemente no hace nada.
    """
    inscripcion = _obtener_inscripcion(inscripcion_id)
    if not inscripcion:
        return {"asignado": False, "motivo": "Inscripción no encontrada"}

    # Si ya existe un seguimiento para esta inscripción, no se duplica.
    if existe_seguimiento(inscripcion_id):
        return {"asignado": False,
                "motivo": "El estudiante ya tiene un profesor asignado"}

    nota = inscripcion["nota_corte1"]
    if not esta_en_riesgo(nota):
        return {"asignado": False, "motivo": "El estudiante no está en riesgo"}

    # Profesores expertos en la materia que el estudiante necesita reforzar.
    profesores = obtener_profesores_de_materia(inscripcion["materia_id"])
    if not profesores:
        return {"asignado": False,
                "motivo": "No hay profesores registrados para esta materia"}

    # Asignación ALEATORIA entre los profesores expertos de la materia.
    profesor_elegido = random.choice(profesores)
    seguimiento_id = crear_seguimiento(inscripcion_id, profesor_elegido["id"], nota)

    # Se asignan al estudiante unas actividades iniciales de refuerzo.
    for descripcion in TAREAS_INICIALES:
        crear_tarea(seguimiento_id, descripcion)

    return {
        "asignado": True,
        "profesor_id": profesor_elegido["id"],
        "profesor": f"{profesor_elegido['nombre']} {profesor_elegido['apellido']}",
        "materia": inscripcion["materia_nombre"],
        "motivo": "Estudiante en riesgo: profesor experto asignado automáticamente",
    }
