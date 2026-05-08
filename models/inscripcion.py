from database.init_db import get_connection

def registrar_inscripcion(estudiante_id, materia_id):
    """Registra la relación entre un estudiante y una materia en Oracle"""
    conn = get_connection()
    cursor = conn.cursor()

    # 2. Oracle usa :1, :2 o parámetros nombrados (:estudiante_id)
    cursor.execute("""
        INSERT INTO inscripciones (estudiante_id, materia_id)
        VALUES (:estudiante_id, :materia_id)
    """, {
        "estudiante_id": estudiante_id, 
        "materia_id": materia_id
    })

    conn.commit()
    cursor.close()
    conn.close()

def listar_inscripciones():
    """Retorna todas las inscripciones con los nombres de estudiantes y materias"""
    conn = get_connection()
    cursor = conn.cursor()

    # 3. La concatenación en Oracle con '||' es igual, pero 
    # manejamos el resultado manualmente para el diccionario.
    cursor.execute("""
        SELECT 
            i.id,
            e.nombre || ' ' || e.apellido AS estudiante,
            m.nombre AS materia,
            i.nota_corte1
        FROM inscripciones i
        JOIN estudiantes e ON i.estudiante_id = e.id
        JOIN materias m ON i.materia_id = m.id
    """)

    rows = cursor.fetchall()
    
    inscripciones = []
    for row in rows:
        inscripciones.append({
            "id": row[0],
            "estudiante": row[1],
            "materia": row[2],
            "nota_corte1": row[3]
        })

    cursor.close()
    conn.close()
    return inscripciones

def actualizar_notas(inscripcion_id, nota_corte1):
    """Actualiza la nota del primer corte para una inscripción específica"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE inscripciones 
        SET nota_corte1 = :nota 
        WHERE id = :id
    """, {"nota": nota_corte1, "id": inscripcion_id})

    conn.commit()
    cambios = cursor.rowcount
    
    cursor.close()
    conn.close()
    return cambios