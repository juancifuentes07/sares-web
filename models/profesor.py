from database.init_db import get_connection

def crear_profesor(nombre, apellido):
    """Inserta un nuevo profesor en la base de datos Oracle XE"""
    conn = get_connection()
    cursor = conn.cursor()

    # 2. Oracle usa parámetros nombrados (:nombre) en lugar de '?'
    cursor.execute("""
        INSERT INTO profesores (nombre, apellido)
        VALUES (:nombre, :apellido)
    """, {"nombre": nombre, "apellido": apellido})

    conn.commit()
    cursor.close()
    conn.close()

def obtener_profesores():
    """Recupera la lista de profesores desde Oracle"""
    conn = get_connection()
    cursor = conn.cursor()

    # 3. Consulta sobre la tabla real en Oracle
    cursor.execute("SELECT id, nombre, apellido FROM profesores")
    rows = cursor.fetchall()

    # 4. Mapeo manual a diccionario para compatibilidad con el frontend
    profesores = []
    for row in rows:
        profesores.append({
            "id": row[0],
            "nombre": row[1],
            "apellido": row[2]
        })

    cursor.close()
    conn.close()
    return profesores