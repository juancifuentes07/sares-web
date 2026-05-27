"""Rutas de la página del profesor (sin login).

- /profesor          : selector para elegir qué profesor ver.
- /profesor/<id>     : panel del profesor con el rendimiento de sus estudiantes.
"""

from flask import Blueprint, render_template, abort
from services.simulacion_service import simular_mejora
from models.profesor import obtener_profesores, obtener_profesor_por_id
from models.seguimiento import obtener_seguimientos_de_profesor
from models.tarea import obtener_tareas_de_seguimiento

profesor_bp = Blueprint("profesor", __name__)


@profesor_bp.route("/profesor")
def seleccionar_profesor():
    """Pantalla de entrada: lista de profesores para elegir cuál ver."""
    profesores = obtener_profesores()
    return render_template("seleccionar_profesor.html", profesores=profesores)


@profesor_bp.route("/profesor/<int:profesor_id>")
def panel_profesor(profesor_id):
    """Panel de un profesor: estudiantes que acompaña y su rendimiento."""
    profesor = obtener_profesor_por_id(profesor_id)
    if not profesor:
        abort(404)

    seguimientos = obtener_seguimientos_de_profesor(profesor_id)

    estudiantes = []
    total_por_hacer = 0
    for s in seguimientos:
        nota_actual  = float(s["nota_actual"])  if s["nota_actual"]  else 0
        nota_inicial = float(s["nota_inicial"]) if s["nota_inicial"] else 0
        proyeccion = simular_mejora(nota_actual) if nota_actual > 0 else None

        # Tendencia respecto a la nota con la que entró en seguimiento.
        if nota_actual > nota_inicial:
            tendencia = "mejorando"
        elif nota_actual < nota_inicial:
            tendencia = "bajando"
        else:
            tendencia = "estable"

        fecha = s["fecha_asignacion"]
        fecha_str = fecha.strftime("%Y-%m-%d") if hasattr(fecha, "strftime") else str(fecha)

        # Actividades que el profesor asignó a este estudiante.
        tareas = obtener_tareas_de_seguimiento(s["seguimiento_id"])
        por_hacer = [t for t in tareas if t["estado"] == "por_hacer"]
        hechas    = [t for t in tareas if t["estado"] == "hecha"]
        total_por_hacer += len(por_hacer)

        estudiantes.append({
            "seguimiento_id": s["seguimiento_id"],
            "estudiante": s["estudiante"],
            "documento": s["documento_estudiante"],
            "materia": s["materia"],
            "nota_inicial": nota_inicial,
            "nota_actual": nota_actual,
            "proyeccion": proyeccion,
            "tendencia": tendencia,
            "estado": s["estado"],
            "fecha_asignacion": fecha_str,
            "tareas": tareas,
            "num_por_hacer": len(por_hacer),
            "num_hechas": len(hechas),
        })

    return render_template("panel_profesor.html",
        profesor=profesor,
        estudiantes=estudiantes,
        total_por_hacer=total_por_hacer)
