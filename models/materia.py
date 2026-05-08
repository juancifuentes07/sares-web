from database.init_db import get_connection


def crear_materia(nombre, carrera):
    """Inserta una nueva materia en el esquema de Oracle"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 2. Usamos parámetros nombrados (:nombre) para mayor claridad en Oracle
    cursor.execute("""
        INSERT INTO materias (nombre, carrera)
        VALUES (:nombre, :carrera)
    """, {"nombre": nombre, "carrera": carrera})
    
    conn.commit()
    cursor.close()
    conn.close()

def obtener_materias():
    """Consulta las 46 materias reales desde Oracle XE"""
    conn = get_connection()
    cursor = conn.cursor()

    # 3. Ejecutamos la consulta sobre la tabla real
    cursor.execute("""
        SELECT id, nombre, carrera
        FROM materias
    """)
    
    rows = cursor.fetchall()
    
    # 4. Mapeo manual de los resultados a diccionario
    materias = []
    for row in rows:
        materias.append({
            "id": row[0],
            "nombre": row[1],
            "carrera": row[2]
        })
    
    cursor.close()
    conn.close()
    
    return materias