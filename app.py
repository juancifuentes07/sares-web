from flask import Flask, request, jsonify
from database.init_db import init_db
from services.estudiante_service import registrar_estudiante, listar_estudiantes
from services.estudiante_service import obtener_estudiante
from services.estudiante_service import borrar_estudiante
from services.profesor_service import registrar_profesor, listar_profesores
from services.materia_service import registrar_materia, listar_materias
from services.inscripcion_service import actualizar_notas, registrar_inscripcion, listar_inscripciones
from services.simulacion_service import simular_mejora
from utils.exceptions import APIError
from flask import render_template
from routes.materia_routes import materia_bp
import sqlite3

app = Flask(__name__)
app.json.ensure_ascii = False
app.register_blueprint(materia_bp)

@app.route("/proyeccion/<int:inscripcion_id>")
def proyeccion(inscripcion_id):
    return {"inscripcion": inscripcion_id}

@app.route("/")
def index():
    return "SARES"

@app.route("/estudiantes", methods=["POST"])
def crear_estudiante():
    response, status = registrar_estudiante(request.get_json())
    return jsonify(response), status

@app.route("/estudiantes", methods=["GET"])
def obtener_estudiantes():
    response, status = listar_estudiantes()
    return jsonify(response), status

@app.route("/estudiantes/<int:id>", methods=["GET"])
def obtener_estudiante_por_id(id):
    response, status = obtener_estudiante(id)
    return jsonify(response), status

@app.route("/estudiantes/<int:id>", methods=["DELETE"])
def eliminar_estudiante_route(id):
    response, status = borrar_estudiante(id)
    return jsonify(response), status

@app.route("/profesores", methods=["POST"])
def crear_profesor_route():
    response, status = registrar_profesor(request.get_json())
    return jsonify(response), status

@app.route("/profesores", methods=["GET"])
def obtener_profesores_route():
    response, status = listar_profesores()
    return jsonify(response), status

@app.route("/materias", methods=["POST"])
def crear_materia_route():
    response, status = registrar_materia(request.get_json())
    return jsonify(response), status

@app.route("/materias", methods=["GET"])
def obtener_materias_route():
    response, status = listar_materias()
    return jsonify(response), status  

@app.route("/inscripciones", methods=["POST"])
def crear_inscripcion_route():
    response, status = registrar_inscripcion(request.get_json())
    return jsonify(response), status

@app.route("/inscripciones", methods=["GET"])
def obtener_inscripciones_route():
    response, status = listar_inscripciones()
    return jsonify(response), status

@app.route("/inscripciones/<int:id>/notas", methods=["PUT"])
def actualizar_notas_route(id):
    data = request.get_json()
    response, status = actualizar_notas(id, data)
    return jsonify(response), status

@app.errorhandler(APIError)
def handle_api_error(error):
    response = {
        "error": error.message
    }
    return jsonify(response), error.status_code

@app.route("/simular-mejora", methods=["POST"])
def simular_mejora_endpoint():

    data = request.get_json()

    nota = data.get("nota_corte1")

    if nota is None:
        raise APIError("Debe enviar la nota del primer corte", 400)

    resultado = simular_mejora(float(nota))

    return jsonify(resultado), 200

@app.route("/simulacion")
def pagina_simulacion():
    return render_template("simulacion.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/materias", methods=["GET"])
def obtener_materias():

    conn = sqlite3.connect("sares.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, carrera, semestre
        FROM materias
        ORDER BY semestre
    """)

    materias = cursor.fetchall()
    conn.close()

    lista_materias = []

    for m in materias:
        lista_materias.append({
            "id": m[0],
            "nombre": m[1],
            "carrera": m[2],
            "semestre": m[3]
        })

    return jsonify(lista_materias)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)