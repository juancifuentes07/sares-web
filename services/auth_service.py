from werkzeug.security import check_password_hash
from models.estudiante import obtener_estudiante_por_documento
import time

_intentos_fallidos = {}

MAX_INTENTOS = 3
BLOQUEO_SEGUNDOS = 30 

def login_estudiante(documento, password):
    ahora = time.time()
    registro = _intentos_fallidos.get(documento, {"intentos": 0, "bloqueado_hasta": 0})
    
    if ahora < registro["bloqueado_hasta"]:
        segundos_restantes = int(registro["bloqueado_hasta"] - ahora)
        return None, f"Cuenta bloqueada. Intente nuevamente en {segundos_restantes} segundos."

    estudiante = obtener_estudiante_por_documento(documento)

    if not check_password_hash(estudiante["password_hash"], password):
        registro["intentos"] += 1
        if registro["intentos"] >= MAX_INTENTOS:
            registro["bloqueado_hasta"] = ahora + BLOQUEO_SEGUNDOS
            _intentos_fallidos[documento] = registro
            return None, f"Demasiados intentos fallidos. Cuenta bloqueada por {BLOQUEO_SEGUNDOS} segundos."
        _intentos_fallidos[documento] = registro
        return None, "Documento o contraseña incorrecta."
    
    _intentos_fallidos.pop(documento, None)
    return estudiante, None

    if not estudiante:
        return None, "Documento no registrado"

    if not check_password_hash(estudiante["password_hash"], password):
        return None, "Contraseña incorrecta"

    return estudiante, None