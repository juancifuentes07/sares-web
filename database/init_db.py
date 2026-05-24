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
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            sql_commands = f.read().split(';')
            
            for command in sql_commands:
                comando_limpio = command.strip()
                if comando_limpio:
                    try:
                        cursor.execute(comando_limpio)
                    except oracledb.DatabaseError as e:
                        error_obj, = e.args
                        # Código 955 = La tabla ya existe. Lo ignoramos para que no falle.
                        if error_obj.code == 955:
                            pass 
                        else:
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