from flask import Blueprint, render_template, request
from services.materia_service import registrar_materia

materia_bp = Blueprint("materia", __name__)

@materia_bp.route("/registrar_materia", methods=["GET","POST"])
def registrar():

    if request.method == "POST":

        estudiante_id = request.form["estudiante_id"]
        carrera = request.form["carrera"]
        materia = request.form["materia"]
        semestre = request.form["semestre"]

        registrar_materia(estudiante_id, carrera, materia, semestre)

        return "Materia registrada correctamente"

    return render_template("registrar_materia.html")