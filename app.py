import os
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from config import Config  # Importamos tu configuración de Oracle
from database.init_db import init_db, get_connection 
from services.estudiante_service import registrar_estudiante, listar_estudiantes, obtener_estudiante, borrar_estudiante
from services.profesor_service import registrar_profesor, listar_profesores
from services.materia_service import registrar_materia, listar_materias
from services.inscripcion_service import actualizar_notas, registrar_inscripcion, listar_inscripciones
from services.simulacion_service import simular_mejora
from utils.exceptions import APIError
from routes.materia_routes import materia_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)

app.secret_key = "sares_secret_2025"
app.config['SESSION_PERMANENT'] = False

# --- Configuración de la Aplicación ---
# Cargamos la configuración de Oracle desde tu clase Config
app.config.from_object(Config)
# Desactivamos ASCII para que se vean bien las tildes de tus 46 materias
app.json.ensure_ascii = False

# Registro de Blueprints
app.register_blueprint(materia_bp)

app.register_blueprint(auth_bp)

# --- Rutas de Lógica Específica ---

@app.route("/proyeccion/<int:inscripcion_id>")
def proyeccion(inscripcion_id):
    """Obtiene la nota de Oracle, calcula la proyección y muestra detalles con actividades"""
    if "estudiante_id" not in session:
        return redirect(url_for("auth.login"))
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Obtener información de la inscripción
    cursor.execute("""
        SELECT i.id, i.nota_corte1, m.nombre, m.id
        FROM inscripciones i
        JOIN materias m ON i.materia_id = m.id
        WHERE i.id = :id AND i.estudiante_id = :est_id
    """, {"id": inscripcion_id, "est_id": session["estudiante_id"]})
    
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        raise APIError("Inscripción no encontrada", 404)
    
    inscripcion_id, nota, nombre_materia, materia_id = row
    
    if nota is None:
        raise APIError("El estudiante no tiene registrada la nota del primer corte", 400)
    
    resultado = simular_mejora(float(nota))
    
    return render_template("proyeccion_detalle.html",
        nombre_materia=nombre_materia,
        materia_id=materia_id,
        inscripcion_id=inscripcion_id,
        resultado=resultado,
        nombre=session.get("estudiante_nombre", "Estudiante")
    )

# --- Rutas de Renderizado de Plantillas (Frontend) ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/simulacion")
def pagina_simulacion():
    return render_template("simulacion.html")

@app.route("/registro")
def registro():
    # 2. Las pasamos al template para que el ciclo 'for' las reconozca
    return render_template("registro.html")

@app.route('/logout_f5')
def logout_f5():
    session.clear()
    return redirect(url_for('index'))

@app.route("/registrar_materia")
def form_inscripcion():
    # Listamos las materias directamente de Oracle para el formulario
    materias, _ = listar_materias()
    return render_template("registrar_materia.html", materias=materias)

@app.after_request
def agregar_cabeceras_seguridad(response):
    # Forzamos una política estricta y limpia para OWASP ZAP
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "img-src 'self' data:; "
        "font-src 'self' data: https://fonts.gstatic.com; "
        "object-src 'none'; "
        "frame-ancestors 'none';"
    )
    response.headers['Content-Security-Policy'] = csp
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    
    # SOLUCIÓN ALERTA WERKZEUG: Pisamos el nombre del servidor para que no revele la versión
    response.headers['Server'] = 'Secure-Server'
    
    return response


# --- Endpoints de la API ---


@app.route('/estudiantes', methods=['POST'])
def registrar_estudiante_route():
    data = request.get_json()

    acepta_tratamiento = data.get('acepta_tratamiento')

    if not acepta_tratamiento:
        return jsonify({"error": "Debe aceptar el tratamiento de datos"}), 400

    response, status = registrar_estudiante(data)

    if status == 201:
        # Auto-login después del registro
        session["estudiante_id"] = response.get("estudiante_id")
        session["estudiante_nombre"] = response.get("nombre")

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
    # Con este IF evitamos que el "debug" de Flask sature los canales de Oracle
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        print("--- Servidor listo para registrar estudiantes en Oracle ---")
        
    app.run(debug=True, host='0.0.0.0', port=5000)