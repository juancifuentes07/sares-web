from functools import wraps
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from services.auth_service import login_estudiante
from services.simulacion_service import simular_mejora
from database.init_db import get_connection

auth_bp = Blueprint("auth", __name__)

def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if "estudiante_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorador

@auth_bp.route("/login", methods=["GET"])
def login():
    if "estudiante_id" in session:
        return redirect(url_for("auth.dashboard"))
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login_post():
    data = request.get_json()
    documento = data.get("documento", "").strip()
    password  = data.get("password", "")

    if not documento or not password:
        return jsonify({"error": "Faltan datos"}), 400

    estudiante, error = login_estudiante(documento, password)

    if error:
        return jsonify({"error": error}), 401

    session["estudiante_id"]     = estudiante["id"]
    session["estudiante_nombre"] = estudiante["nombre"]

    return jsonify({"mensaje": "Login exitoso"}), 200

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@auth_bp.route("/dashboard")
@login_requerido
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id, m.nombre, i.nota_corte1
        FROM inscripciones i
        JOIN materias m ON i.materia_id = m.id
        WHERE i.estudiante_id = :id
    """, {"id": session["estudiante_id"]})
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    materias = []
    for row in rows:
        nota = float(row[2]) if row[2] else 0
        proyeccion = simular_mejora(nota) if nota > 0 else None

        if nota == 0:
            estado = "sin_nota"
        elif proyeccion and proyeccion["nota_final_estimada"] >= 3.0:
            estado = "estable"
        else:
            estado = "riesgo"

        materias.append({
            "inscripcion_id": row[0],
            "nombre": row[1],
            "nota": nota,
            "estado": estado,
            "proyeccion": proyeccion
        })

    return render_template("dashboard.html",
        nombre=session["estudiante_nombre"],
        materias=materias
    )