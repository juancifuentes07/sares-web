from database.init_db import get_connection


def crear_estudiante(nombre, apellido, documento, carrera):
    """Inserta un estudiante en la tabla de Oracle"""
    conn = get_connection()
    cursor = conn.cursor()

    # 2. En Oracle usamos :nombre o :1 en lugar de ?
    cursor.execute("""
        INSERT INTO estudiantes (nombre, apellido, documento, carrera)
        VALUES (:nombre, :apellido, :documento, :carrera)
    """, {
        "nombre": nombre, 
        "apellido": apellido, 
        "documento": documento, 
        "carrera": carrera
    })

    conn.commit()
    cursor.close()
    conn.close()

def obtener_estudiantes():
    """Recupera todos los registros de la tabla estudiantes en Oracle"""
    conn = get_connection()
    cursor = conn.cursor()

    # 3. Especificamos las columnas para mapear el diccionario manualmente
    cursor.execute("SELECT id, nombre, apellido, documento, carrera FROM estudiantes")
    rows = cursor.fetchall()

    estudiantes = []
    for row in rows:
        estudiantes.append({
            "id": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "documento": row[3],
            "carrera": row[4]
        })

    cursor.close()
    conn.close()
    return estudiantes

def obtener_estudiante_por_id(estudiante_id):
    """Busca un estudiante específico por su ID único"""
    conn = get_connection()
    cursor = conn.cursor()

    # 4. Sintaxis de parámetros nombrados para Oracle
    cursor.execute("SELECT id, nombre, apellido, documento, carrera FROM estudiantes WHERE id = :id", {"id": estudiante_id})
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "documento": row[3],
            "carrera": row[4]
        }
    return None

def eliminar_estudiante(estudiante_id):
    """Borra un estudiante y retorna cuántas filas fueron afectadas"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM estudiantes WHERE id = :id", {"id": estudiante_id})
    
    conn.commit()
    cambios = cursor.rowcount
    
    cursor.close()
    conn.close()

    return cambios