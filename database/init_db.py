import os
import sys
import oracledb

# Permite ejecutar este módulo directamente desde la raíz del proyecto o desde otro lugar.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from config import Config

_pool = None

def get_pool():
    global _pool
    if _pool is None:
        _pool = oracledb.create_pool(
            user=Config.USUARIO,
            password=Config.PASSWORD,
            dsn=f"{Config.HOST}:{Config.PUERTO}/{Config.SERVICIO}",
            min=5,
            max=20,
            increment=2
        )
    return _pool

def get_connection():
    # Usa la configuración que guardaste en config.py
    return get_pool().acquire()

def _is_ignorable_error(error_obj):
    # Código 955 = tabla ya existe
    # Código 1 = restricción única violada (registro ya existe)
    return error_obj.code in (955, 1)


def init_db():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql_commands = f.read().split(';')

            for command in sql_commands:
                comando_limpio = command.strip()
                if not comando_limpio:
                    continue

                try:
                    cursor.execute(comando_limpio)
                except oracledb.DatabaseError as e:
                    error_obj, = e.args
                    if _is_ignorable_error(error_obj):
                        continue
                    print(f"Aviso SQL (Código {error_obj.code}): {error_obj.message}")

        conn.commit()
        print("¡Estructura de base de datos verificada con éxito!")

    except Exception as e:
        print(f"Error en init_db durante el arranque: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            try:
                get_pool().release(conn)
            except Exception:
                pass


if __name__ == '__main__':
    init_db()
