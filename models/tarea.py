import oracledb
from database.init_db import get_connection


def crear_tarea(seguimiento_id, descripcion):
    """Crea una actividad que el profesor asigna al estudiante.
    Devuelve el id generado."""
    conn = get_connection()
    cursor = conn.cursor()
    id_var = cursor.var(oracledb.NUMBER)
    cursor.execute("""
        INSERT INTO tareas (seguimiento_id, descripcion)
        VALUES (:sid, :desc)
        RETURNING id INTO :id_out
    """, {"sid": seguimiento_id, "desc": descripcion, "id_out": id_var})
    conn.commit()
    nuevo_id = int(id_var.getvalue()[0])
    cursor.close()
    conn.close()
    return nuevo_id


def obtener_tareas_de_seguimiento(seguimiento_id):
    """Devuelve las actividades asignadas a un estudiante (un seguimiento).
    Las que están 'por_hacer' aparecen primero."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, descripcion, estado, fecha_creacion
        FROM tareas
        WHERE seguimiento_id = :sid
        ORDER BY estado ASC, fecha_creacion
    """, {"sid": seguimiento_id})
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": r[0], "descripcion": r[1], "estado": r[2],
             "fecha_creacion": r[3]} for r in rows]


def cambiar_estado_tarea(tarea_id, estado):
    """Marca una actividad como 'por_hacer' o 'hecha'."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tareas SET estado = :estado WHERE id = :id",
        {"estado": estado, "id": tarea_id}
    )
    conn.commit()
    cambios = cursor.rowcount
    cursor.close()
    conn.close()
    return cambios
