"""Rutas para gestionar seguimientos y tareas desde la página del profesor.

Sin login: la página del profesor es de solo lectura ampliada. Estas rutas
permiten marcar tareas como hechas y registrar observaciones.
"""

from flask import Blueprint, request, jsonify
from models.seguimiento import actualizar_estado
from models.tarea import cambiar_estado_tarea, crear_tarea

seguimiento_bp = Blueprint("seguimiento", __name__)

ESTADOS_SEGUIMIENTO = {"en_seguimiento", "mejorado", "cerrado"}
ESTADOS_TAREA = {"pendiente", "hecha"}


@seguimiento_bp.route("/seguimientos/<int:seguimiento_id>", methods=["PUT"])
def actualizar_seguimiento(seguimiento_id):
    """Actualiza el estado y/o las observaciones de un seguimiento."""
    data = request.get_json() or {}
    estado        = data.get("estado")
    observaciones = data.get("observaciones")

    if estado is not None and estado not in ESTADOS_SEGUIMIENTO:
        return jsonify({"error": "Estado no válido"}), 400
    if estado is None and observaciones is None:
        return jsonify({"error": "Nada que actualizar"}), 400

    actualizar_estado(
        seguimiento_id,
        estado if estado is not None else "en_seguimiento",
        observaciones,
    )
    return jsonify({"mensaje": "Seguimiento actualizado correctamente"}), 200


@seguimiento_bp.route("/tareas/<int:tarea_id>", methods=["PUT"])
def actualizar_tarea(tarea_id):
    """Marca una tarea como 'pendiente' o 'hecha'."""
    data = request.get_json() or {}
    estado = data.get("estado")

    if estado not in ESTADOS_TAREA:
        return jsonify({"error": "Estado no válido"}), 400

    cambios = cambiar_estado_tarea(tarea_id, estado)
    if cambios == 0:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify({"mensaje": "Tarea actualizada"}), 200


@seguimiento_bp.route("/seguimientos/<int:seguimiento_id>/tareas", methods=["POST"])
def agregar_tarea(seguimiento_id):
    """Agrega una nueva tarea (trabajo por realizar) a un seguimiento."""
    data = request.get_json() or {}
    descripcion = (data.get("descripcion") or "").strip()

    if not descripcion:
        return jsonify({"error": "La descripción no puede estar vacía"}), 400

    nuevo_id = crear_tarea(seguimiento_id, descripcion)
    return jsonify({"mensaje": "Tarea agregada", "id": nuevo_id}), 201