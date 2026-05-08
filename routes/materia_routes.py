from flask import Blueprint, render_template, request
from services.materia_service import listar_materias, registrar_materia

materia_bp = Blueprint("materia", __name__)

@materia_bp.route("/registrar_materia", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre"),
            "carrera": request.form.get("carrera")
        }
        registrar_materia(data)
        return "Materia registrada correctamente"

    materias, _ = listar_materias()
    return render_template("registrar_materia.html", materias=materias)
