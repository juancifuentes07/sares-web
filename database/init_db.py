import oracledb
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

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Aquí es donde fallaba: Oracle no usa 'executescript' de la misma forma que SQLite
    with open('database/schema.sql', 'r', encoding='utf-8') as f:
        sql_commands = f.read().split(';')
        for command in sql_commands:
            if command.strip():
                cursor.execute(command)
                pass
            
    conn.commit()
    cursor.close()
    conn.close()