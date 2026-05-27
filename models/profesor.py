from database.init_db import get_connection
import oracledb


def crear_profesor(nombre, apellido, documento=None):
    """Inserta un nuevo profesor en la base de datos Oracle XE.

    Devuelve el id generado. El parámetro documento es opcional para
    mantener compatibilidad con llamadas antiguas.
    """
    conn = get_connection()
    cursor = conn.cursor()

    id_var = cursor.var(oracledb.NUMBER)
    cursor.execute("""
        INSERT INTO profesores (nombre, apellido, documento)
        VALUES (:nombre, :apellido, :documento)
        RETURNING id INTO :id_out
    """, {
        "nombre": nombre,
        "apellido": apellido,
        "documento": documento,
        "id_out": id_var
    })

    conn.commit()
    nuevo_id = int(id_var.getvalue()[0])
    cursor.close()
    conn.close()
    return nuevo_id


def obtener_profesores():
    """Recupera la lista de profesores desde Oracle, con las materias
    en que cada uno es experto."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre, apellido, documento FROM profesores ORDER BY id")
    rows = cursor.fetchall()

    profesores = []
    for row in rows:
        cursor.execute("""
            SELECT m.id, m.nombre
            FROM profesor_materia pm
            JOIN materias m ON pm.materia_id = m.id
            WHERE pm.profesor_id = :pid
        """, {"pid": row[0]})
        materias = [{"id": m[0], "nombre": m[1]} for m in cursor.fetchall()]
        profesores.append({
            "id": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "documento": row[3],
            "materias": materias
        })

    cursor.close()
    conn.close()
    return profesores


def obtener_profesor_por_id(profesor_id):
    """Devuelve los datos de un profesor concreto."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre, apellido, documento
        FROM profesores WHERE id = :id
    """, {"id": profesor_id})
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return {"id": row[0], "nombre": row[1],
                "apellido": row[2], "documento": row[3]}
    return None


# ----------------------------------------------------------------
# Relación profesor <-> materia (muchos a muchos)
# ----------------------------------------------------------------
def asignar_materia_a_profesor(profesor_id, materia_id):
    """Marca a un profesor como experto en una materia.
    Si el vínculo ya existe, MERGE evita el error de clave duplicada."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        MERGE INTO profesor_materia pm
        USING (SELECT :pid AS profesor_id, :mid AS materia_id FROM dual) src
        ON (pm.profesor_id = src.profesor_id AND pm.materia_id = src.materia_id)
        WHEN NOT MATCHED THEN
            INSERT (profesor_id, materia_id)
            VALUES (src.profesor_id, src.materia_id)
    """, {"pid": profesor_id, "mid": materia_id})
    conn.commit()
    cursor.close()
    conn.close()


def obtener_profesores_de_materia(materia_id):
    """Devuelve los profesores expertos en una materia (lista de dicts)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.nombre, p.apellido
        FROM profesor_materia pm
        JOIN profesores p ON pm.profesor_id = p.id
        WHERE pm.materia_id = :mid
        ORDER BY p.id
    """, {"mid": materia_id})
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": r[0], "nombre": r[1], "apellido": r[2]} for r in rows]
