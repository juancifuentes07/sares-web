import oracledb
from database.init_db import get_connection


def existe_seguimiento(inscripcion_id):
    """True si la inscripción ya tiene un seguimiento (en cualquier estado)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM seguimientos WHERE inscripcion_id = :id",
        {"id": inscripcion_id}
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row is not None


def crear_seguimiento(inscripcion_id, profesor_id, nota_inicial):
    """Crea un seguimiento académico para una inscripción en riesgo.
    Devuelve el id generado."""
    conn = get_connection()
    cursor = conn.cursor()

    id_var = cursor.var(oracledb.NUMBER)
    cursor.execute("""
        INSERT INTO seguimientos (inscripcion_id, profesor_id, nota_inicial)
        VALUES (:inscripcion_id, :profesor_id, :nota_inicial)
        RETURNING id INTO :id_out
    """, {
        "inscripcion_id": inscripcion_id,
        "profesor_id": profesor_id,
        "nota_inicial": nota_inicial,
        "id_out": id_var
    })

    conn.commit()
    nuevo_id = int(id_var.getvalue()[0])
    cursor.close()
    conn.close()
    return nuevo_id


def obtener_seguimientos_de_profesor(profesor_id):
    """Devuelve todos los estudiantes que un profesor sigue, con su progreso."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            s.id,
            s.estado,
            s.nota_inicial,
            s.fecha_asignacion,
            s.observaciones,
            i.id,
            i.nota_corte1,
            m.nombre,
            e.nombre || ' ' || e.apellido,
            e.documento
        FROM seguimientos s
        JOIN inscripciones i ON s.inscripcion_id = i.id
        JOIN materias m      ON i.materia_id     = m.id
        JOIN estudiantes e   ON i.estudiante_id  = e.id
        WHERE s.profesor_id = :pid
        ORDER BY s.estado ASC, s.fecha_asignacion DESC
    """, {"pid": profesor_id})
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    seguimientos = []
    for r in rows:
        # Las observaciones pueden venir como LOB en Oracle; se convierten a str.
        observaciones = r[4]
        if observaciones is not None and hasattr(observaciones, "read"):
            observaciones = observaciones.read()
        seguimientos.append({
            "seguimiento_id": r[0],
            "estado": r[1],
            "nota_inicial": r[2],
            "fecha_asignacion": r[3],
            "observaciones": observaciones or "",
            "inscripcion_id": r[5],
            "nota_actual": r[6],
            "materia": r[7],
            "estudiante": r[8],
            "documento_estudiante": r[9],
        })
    return seguimientos


def actualizar_estado(seguimiento_id, estado, observaciones=None):
    """Actualiza el estado del seguimiento y, opcionalmente, las observaciones."""
    conn = get_connection()
    cursor = conn.cursor()
    if observaciones is not None:
        cursor.execute("""
            UPDATE seguimientos
            SET estado = :estado, observaciones = :obs
            WHERE id = :id
        """, {"estado": estado, "obs": observaciones, "id": seguimiento_id})
    else:
        cursor.execute("""
            UPDATE seguimientos SET estado = :estado WHERE id = :id
        """, {"estado": estado, "id": seguimiento_id})
    conn.commit()
    cambios = cursor.rowcount
    cursor.close()
    conn.close()
    return cambios
