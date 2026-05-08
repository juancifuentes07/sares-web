import oracledb
# Sincronizamos los nombres según tu modelo de Oracle
from models.inscripcion import registrar_inscripcion as db_registrar_inscripcion, listar_inscripciones as db_listar_inscripciones
from database.init_db import get_connection
from utils.exceptions import APIError

def registrar_inscripcion(data):
    estudiante_id = data.get("estudiante_id")
    materia_id = data.get("materia_id")

    if not all([estudiante_id, materia_id]):
        return {"error": "Faltan datos"}, 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 🔎 En Oracle usamos :id en lugar de ?
        cursor.execute("SELECT id FROM estudiantes WHERE id = :id", {"id": estudiante_id})
        if not cursor.fetchone():
            return {"error": "El estudiante no existe"}, 404

        # 🔎 Verificar que la materia exista
        cursor.execute("SELECT id FROM materias WHERE id = :id", {"id": materia_id})
        if not cursor.fetchone():
            return {"error": "La materia no existe"}, 404

        # 🔎 Verificar duplicados
        cursor.execute("""
            SELECT id FROM inscripciones 
            WHERE estudiante_id = :est_id AND materia_id = :mat_id
        """, {"est_id": estudiante_id, "mat_id": materia_id})

        if cursor.fetchone():
            return {"error": "El estudiante ya está inscrito en esta materia"}, 400

        # ✅ Realizar la inserción
        cursor.execute("""
            INSERT INTO inscripciones (estudiante_id, materia_id)
            VALUES (:est_id, :mat_id)
        """, {"est_id": estudiante_id, "mat_id": materia_id})

        conn.commit()
        return {"mensaje": "Inscripción realizada correctamente"}, 201

    except oracledb.Error as e:
        return {"error": f"Error en Oracle: {str(e)}"}, 500
    finally:
        cursor.close()
        conn.close()

# --- CAMBIO CRÍTICO AQUÍ PARA SOLUCIONAR EL ERROR DE image_1d9933.png ---
def listar_inscripciones():
    """
    Se renombró de 'obtener_inscripciones_servicio' a 'listar_inscripciones'
    para coincidir con la importación en app.py.
    """
    return db_listar_inscripciones(), 200

def actualizar_notas(inscripcion_id, data):
    nota1 = data.get("nota_corte1")

    if nota1 is None:
        return {"error": "La nota es obligatoria"}, 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 🔎 Update con sintaxis Oracle
        cursor.execute("""
            UPDATE inscripciones
            SET nota_corte1 = :nota
            WHERE id = :id
        """, {"nota": nota1, "id": inscripcion_id})

        if cursor.rowcount == 0:
            return {"error": "Inscripción no encontrada"}, 404

        conn.commit()
        return {"mensaje": "Notas actualizadas correctamente"}, 200
    
    except oracledb.Error as e:
        return {"error": f"Error al actualizar: {str(e)}"}, 500
    finally:
        cursor.close()
        conn.close()