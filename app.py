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

from routes.materia_routes import materia_bp
from routes.auth_routes import auth_bp
from routes.profesor_routes import profesor_bp
from routes.tarea_routes import tarea_bp

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
app.register_blueprint(profesor_bp)
app.register_blueprint(tarea_bp)
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
 
    nota = float(nota) if nota is not None else 0.0
 
    # Buscar si esta inscripción tiene un profesor de apoyo asignado.
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, p.apellido, s.estado, s.fecha_asignacion
        FROM seguimientos s
        JOIN profesores p ON s.profesor_id = p.id
        WHERE s.inscripcion_id = :id
    """, {"id": inscripcion_id})
    fila_prof = cursor.fetchone()
    cursor.close()
    conn.close()
 
    profesor_asignado = None
    if fila_prof:
        fecha = fila_prof[3]
        fecha_str = fecha.strftime("%Y-%m-%d") if hasattr(fecha, "strftime") else str(fecha)
        profesor_asignado = {
            "nombre": f"{fila_prof[0]} {fila_prof[1]}",
            "estado": fila_prof[2],
            "fecha": fecha_str,
        }
 
    if nota == 0.0:
        return render_template("proyeccion_detalle.html",
            nombre_materia=nombre_materia,
            materia_id=materia_id,
            inscripcion_id=inscripcion_id,
            resultado=None,
            profesor_asignado=profesor_asignado,
            nombre=session.get("estudiante_nombre", "Estudiante")
        )
    resultado = simular_mejora(nota)
 
    return render_template("proyeccion_detalle.html",
        nombre_materia=nombre_materia,
        materia_id=materia_id,
        inscripcion_id=inscripcion_id,
        resultado=resultado,
        profesor_asignado=profesor_asignado,
        nombre=session.get("estudiante_nombre", "Estudiante")
    )
 
# --- Rutas de Renderizado de Plantillas (Frontend) ---
@app.route('/salir_al_index')
def salir_al_index():
    session.clear()  # Borra los datos del usuario del servidor por completo
    return redirect(url_for('index'))  # Te manda al index.html completamente limpio

@app.route('/')
def index():
    # Renderiza tu index sin peligro de arrastrar sesiones
    return render_template('index.html')

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

@app.route("/simuladornotas")
def calculadora_notas():
    """Página independiente de calculadora de notas"""
    return render_template("simuladornotas.html")

@app.route("/simulacion_ingreso_nota/<int:inscripcion_id>")
def ingreso_nota_inicial(inscripcion_id):
    """Formulario para ingresar la nota inicial antes de la simulación"""
    if "estudiante_id" not in session:
        return redirect(url_for("auth.login"))
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Obtener información de la inscripción y materia
    cursor.execute("""
        SELECT i.id, m.nombre
        FROM inscripciones i
        JOIN materias m ON i.materia_id = m.id
        WHERE i.id = :id AND i.estudiante_id = :est_id
    """, {"id": inscripcion_id, "est_id": session["estudiante_id"]})
    
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not row:
        return redirect(url_for("auth.dashboard"))
    
    return render_template("simulacion_ingreso_nota.html", 
        inscripcion_id=inscripcion_id,
        materia_nombre=row[1]
    )
@app.before_request
def limpiar_sesión_en_login():
    # Si el usuario intenta cargar la página de login, le borramos la sesión de inmediato
    if request.path == '/login' and request.method == 'GET':
        session.clear()
        
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

@app.route("/inscripciones/crear", methods=["POST"])
def crear_inscripcion_para_simulacion():
    """Crea una inscripción sin nota inicial, lista para ir a ingreso_nota_inicial"""
    if "estudiante_id" not in session:
        return jsonify({"error": "No autenticado"}), 401
    
    data = request.get_json()
    materia_id = data.get("materia_id")
    
    if not materia_id:
        return jsonify({"error": "materia_id requerido"}), 400
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar si ya existe inscripción
        cursor.execute("""
            SELECT id FROM inscripciones 
            WHERE estudiante_id = :est_id AND materia_id = :mat_id
        """, {"est_id": session["estudiante_id"], "mat_id": materia_id})
        
        existing = cursor.fetchone()
        
        if existing:
            # Ya existe, usar esa inscripción
            inscripcion_id = existing[0]
            cursor.close()
            conn.close()
            return jsonify({"inscripcion_id": inscripcion_id}), 200
        
        # Crear nueva inscripción usando el servicio existente
        cursor.close()
        conn.close()
        
        # Usar el servicio que ya tiene toda la lógica
        response, status = registrar_inscripcion({
            "estudiante_id": session["estudiante_id"],
            "materia_id": materia_id
        })
        
        if status != 201:
            return jsonify(response), status
        
        # La respuesta contiene la inscripción creada
        # Necesito obtener su ID - vamos a consultarlo
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM inscripciones 
            WHERE estudiante_id = :est_id AND materia_id = :mat_id
        """, {"est_id": session["estudiante_id"], "mat_id": materia_id})
        
        inscripcion_id = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        return jsonify({"inscripcion_id": inscripcion_id}), 201
        
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/inscripciones/<int:id>/guardar_nota_inicial", methods=["POST"])
def guardar_nota_inicial(id):
    """Guarda la nota inicial (Corte 1) de una inscripción"""
    if "estudiante_id" not in session:
        return jsonify({"error": "No autenticado"}), 401

    data = request.get_json()
    nota_corte1 = data.get("nota_corte1")

    if nota_corte1 is None:
        return jsonify({"error": "nota_corte1 requerido"}), 400

    try:
        nota_corte1 = float(nota_corte1)
    except ValueError:
        return jsonify({"error": "nota_corte1 debe ser un número"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Verificar que la inscripción pertenece al estudiante
        cursor.execute("""
            SELECT id FROM inscripciones WHERE id = :id AND estudiante_id = :est_id
        """, {"id": id, "est_id": session["estudiante_id"]})

        if not cursor.fetchone():
            return jsonify({"error": "Inscripción no encontrada"}), 404

        # Actualizar la nota
        cursor.execute("""
            UPDATE inscripciones SET nota_corte1 = :nota WHERE id = :id
        """, {"nota": nota_corte1, "id": id})

        conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    # Asignación de profesor: va aparte y protegida, para que un fallo aquí
    # NUNCA tumbe el guardado de la nota ni la respuesta al navegador.
    respuesta = {"mensaje": "Nota guardada correctamente"}
    try:
        from services.asignacion_service import evaluar_y_asignar
        resultado = evaluar_y_asignar(id)
        if resultado.get("asignado"):
            respuesta["asignacion"] = (
                f"Quedaste en riesgo en esta materia. Se te asignó al profesor "
                f"{resultado['profesor']} para acompañar tu proceso."
            )
    except Exception as e:
        # Si la asignación falla, lo registramos pero NO rompemos la respuesta.
        print("Aviso: no se pudo asignar profesor automáticamente:", e)

    return jsonify(respuesta), 200

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