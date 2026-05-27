"""Rutas para gestionar las actividades que el profesor asigna al estudiante.

Sin login: el profesor opera desde su panel.
- Marcar una actividad como hecha / por hacer.
- Agregar una nueva actividad a un estudiante.
"""

from flask import Blueprint, request, jsonify
from models.tarea import cambiar_estado_tarea, crear_tarea

tarea_bp = Blueprint("tarea", __name__)

ESTADOS_TAREA = {"por_hacer", "hecha"}


@tarea_bp.route("/tareas/<int:tarea_id>", methods=["PUT"])
def actualizar_tarea(tarea_id):
    """Marca una actividad como 'por_hacer' o 'hecha'."""
    data = request.get_json() or {}
    estado = data.get("estado")

    if estado not in ESTADOS_TAREA:
        return jsonify({"error": "Estado no válido"}), 400

    cambios = cambiar_estado_tarea(tarea_id, estado)
    if cambios == 0:
        return jsonify({"error": "Actividad no encontrada"}), 404
    return jsonify({"mensaje": "Actividad actualizada"}), 200


@tarea_bp.route("/seguimientos/<int:seguimiento_id>/tareas", methods=["POST"])
def agregar_tarea(seguimiento_id):
    """Agrega una nueva actividad al estudiante dentro de un seguimiento."""
    data = request.get_json() or {}
    descripcion = (data.get("descripcion") or "").strip()

    if not descripcion:
        return jsonify({"error": "La descripción no puede estar vacía"}), 400

    nuevo_id = crear_tarea(seguimiento_id, descripcion)
    return jsonify({"mensaje": "Actividad agregada", "id": nuevo_id}), 201
