from flask import Flask, request, jsonify, render_template
from config import Config  # Importamos tu configuración de Oracle
from database.init_db import init_db, get_connection 
from services.estudiante_service import crear_estudiante as registrar_estudiante, obtener_estudiantes as listar_estudiantes, obtener_estudiante_por_id as obtener_estudiante, eliminar_estudiante as borrar_estudiante
from services.profesor_service import registrar_profesor, listar_profesores
from services.materia_service import registrar_materia, listar_materias
from services.inscripcion_service import actualizar_notas, registrar_inscripcion, listar_inscripciones
from services.simulacion_service import simular_mejora
from utils.exceptions import APIError
from routes.materia_routes import materia_bp

app = Flask(__name__)

app.secret_key = "sares_secret_2025"

# --- Configuración de la Aplicación ---
# Cargamos la configuración de Oracle desde tu clase Config
app.config.from_object(Config)
# Desactivamos ASCII para que se vean bien las tildes de tus 46 materias
app.json.ensure_ascii = False

# Registro de Blueprints
app.register_blueprint(materia_bp)

from routes.auth_routes import auth_bp
app.register_blueprint(auth_bp)

# --- Rutas de Lógica Específica ---

@app.route("/proyeccion/<int:inscripcion_id>")
def proyeccion(inscripcion_id):
    """Obtiene la nota de Oracle y calcula la proyección de mejora"""
    conn = get_connection()
    cursor = conn.cursor()
    # Usamos la sintaxis de Oracle :id para evitar inyección SQL
    cursor.execute("SELECT nota_corte1 FROM inscripciones WHERE id = :id", {"id": inscripcion_id})
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        raise APIError("Inscripción no encontrada", 404)
    
    nota = row[0]
    if nota is None:
        raise APIError("El estudiante no tiene registrada la nota del primer corte", 400)
    
    resultado = simular_mejora(float(nota))
    return jsonify(resultado), 200

# --- Rutas de Renderizado de Plantillas (Frontend) ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/simulacion")
def pagina_simulacion():
    return render_template("simulacion.html")

@app.route("/registro")
def registro():
    # 1. Traemos las materias de Oracle usando el servicio que ya migramos
    materias, _ = listar_materias() 
    # 2. Las pasamos al template para que el ciclo 'for' las reconozca
    return render_template("registro.html", materias=materias)

@app.route("/registrar_materia")
def form_inscripcion():
    # Listamos las materias directamente de Oracle para el formulario
    materias, _ = listar_materias()
    return render_template("registrar_materia.html", materias=materias)

# --- Endpoints de la API ---

@app.route('/estudiantes', methods=['POST'])
def registrar_estudiante_route():
    data = request.get_json()

    acepta_tratamiento = data.get('acepta_tratamiento')

    if not acepta_tratamiento:
        return jsonify({"error": "Debe aceptar el tratamiento de datos"}), 400

    response, status = registrar_estudiante(data)

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
    """Este endpoint debe retornar tus 46 materias de Oracle"""
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

@app.route("/simular-mejora", methods=["POST"])
def simular_mejora_endpoint():
    data = request.get_json()
    nota = data.get("nota_corte1")
    if nota is None:
        raise APIError("Debe enviar la nota del primer corte", 400)
    resultado = simular_mejora(float(nota))
    return jsonify(resultado), 200

# --- Manejo de Errores ---

@app.errorhandler(APIError)
def handle_api_error(error):
    return jsonify({"error": error.message}), error.status_code

# --- Ejecución del Servidor ---

if __name__ == "__main__":  
    # Si las tablas no existen en Oracle, descomenta la siguiente línea una vez:
    # init_db() 
    app.run(debug=True)