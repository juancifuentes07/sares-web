"""
Puebla la tabla de profesores para SARES.

- Crea un conjunto de profesores con nombres realistas.
- Asigna materias de forma que CADA materia tenga al menos DOS profesores
  expertos (requisito para que la asignación aleatoria siempre funcione).

USO (desde la raíz del proyecto, la carpeta sares-web):
    python -m scripts.poblar_profesores

Es seguro re-ejecutarlo: detecta profesores ya existentes por documento.
"""

import random

from database.init_db import get_connection
from models.profesor import crear_profesor, asignar_materia_a_profesor
from models.materia import obtener_materias


NOMBRES = [
    "Carlos", "María", "Jorge", "Diana", "Andrés", "Laura", "Felipe",
    "Sandra", "Ricardo", "Paula", "Miguel", "Carolina", "Javier", "Natalia",
    "Sergio", "Adriana", "Daniel", "Catalina", "Óscar", "Valentina",
]
APELLIDOS = [
    "Ramírez", "López", "Torres", "Castro", "Gómez", "Rodríguez", "Martínez",
    "Hernández", "Díaz", "Vargas", "Moreno", "Rojas", "Jiménez", "Suárez",
    "Mendoza", "Ortiz", "Guerrero", "Cárdenas", "Peña", "Restrepo",
]

NUM_PROFESORES = 20
MATERIAS_POR_PROFESOR = 4
MIN_PROFESORES_POR_MATERIA = 2


def profesor_existe(documento):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM profesores WHERE documento = :doc", {"doc": documento})
    existe = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return existe


def poblar():
    materias = obtener_materias()
    if not materias:
        print("No hay materias en la base de datos. Carga primero las materias.")
        return

    materia_ids = [m["id"] for m in materias]
    print(f"Materias encontradas: {len(materia_ids)}")

    # --- 1. Crear los profesores ---
    profesores_creados = []
    for i in range(NUM_PROFESORES):
        nombre   = random.choice(NOMBRES)
        apellido = random.choice(APELLIDOS)
        documento = f"90{i:08d}"  # documento determinístico para no duplicar

        if profesor_existe(documento):
            print(f"  - Profesor con documento {documento} ya existe, se omite.")
            continue

        try:
            pid = crear_profesor(nombre, apellido, documento)
            profesores_creados.append(pid)
            print(f"  + {nombre} {apellido} (id={pid})")
        except Exception as e:
            print(f"  ! Error creando profesor: {e}")

    if not profesores_creados:
        print("\nNo se crearon profesores nuevos (ya estaban creados).")
        return

    # --- 2. Asignar materias a cada profesor (reparto aleatorio) ---
    cobertura = {mid: 0 for mid in materia_ids}
    for pid in profesores_creados:
        elegidas = random.sample(
            materia_ids, min(MATERIAS_POR_PROFESOR, len(materia_ids))
        )
        for mid in elegidas:
            asignar_materia_a_profesor(pid, mid)
            cobertura[mid] += 1

    # --- 3. Garantizar el mínimo de profesores por materia ---
    for mid, cuenta in cobertura.items():
        while cuenta < MIN_PROFESORES_POR_MATERIA:
            candidatos = list(profesores_creados)
            random.shuffle(candidatos)
            asignado = False
            for pid in candidatos:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    SELECT 1 FROM profesor_materia
                    WHERE profesor_id = :p AND materia_id = :m
                """, {"p": pid, "m": mid})
                ya_dicta = cur.fetchone() is not None
                cur.close()
                conn.close()
                if not ya_dicta:
                    asignar_materia_a_profesor(pid, mid)
                    cuenta += 1
                    asignado = True
                    break
            if not asignado:
                break

    # --- 4. Reporte final ---
    print("\n--- Verificación de cobertura ---")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.nombre, COUNT(pm.profesor_id)
        FROM materias m
        LEFT JOIN profesor_materia pm ON m.id = pm.materia_id
        GROUP BY m.nombre
        ORDER BY COUNT(pm.profesor_id)
    """)
    filas = cursor.fetchall()
    cursor.close()
    conn.close()

    con_pocos = [f for f in filas if f[1] < MIN_PROFESORES_POR_MATERIA]
    print(f"Materias totales: {len(filas)}")
    if con_pocos:
        print("ATENCIÓN: estas materias quedaron con pocos profesores:")
        for nombre, n in con_pocos:
            print(f"  - {nombre}: {n}")
    else:
        print("Todas las materias tienen al menos 2 profesores expertos.")

    print("\nListo. Profesores poblados correctamente.")


if __name__ == "__main__":
    poblar()
