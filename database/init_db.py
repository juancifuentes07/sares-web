import oracledb
from config import Config

def get_connection():
    # Usa la configuración que guardaste en config.py
    return oracledb.connect(
        user=Config.USUARIO,
        password=Config.PASSWORD,
        dsn=f"{Config.HOST}:{Config.PUERTO}/{Config.SERVICIO}"
    )

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Aquí es donde fallaba: Oracle no usa 'executescript' de la misma forma que SQLite
    with open('database/schema.sql', 'r', encoding='utf-8') as f:
        sql_commands = f.read().split(';')
        for command in sql_commands:
            if command.strip():
                cursor.execute(command)
    conn.commit()
    cursor.close()
    conn.close()