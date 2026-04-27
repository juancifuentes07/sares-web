import pytest
import sqlite3
import os
import sys
import tempfile


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.simulacion_service import (
    simular_mejora,
    determinar_iteraciones,
    determinar_k,
    modelo,
)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    documento TEXT NOT NULL UNIQUE,
    carrera TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS profesores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS materias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    carrera TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS inscripciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id INTEGER NOT NULL,
    materia_id INTEGER NOT NULL,
    nota_corte1 REAL DEFAULT 0,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE,
    UNIQUE(estudiante_id, materia_id)
);

INSERT INTO materias (nombre, carrera) VALUES
    ('Cálculo Diferencial', 'Ingeniería de Sistemas'),
    ('Estructuras de Datos', 'Ingeniería de Sistemas'),
    ('Programación I', 'Ingeniería de Sistemas');
"""

@pytest.fixture()
def db_path(tmp_path, monkeypatch):
    db_file = str(tmp_path / "sares_test.db")

    conn = sqlite3.connect(db_file)
    conn.executescript(SCHEMA_SQL)
    conn.close()

    import models.estudiante as m_est
    import models.materia as m_mat
    import models.inscripcion as m_ins
    import models.profesor as m_prof

    monkeypatch.setattr(m_est, "DB_NAME", db_file)
    monkeypatch.setattr(m_mat, "DB_NAME", db_file)
    monkeypatch.setattr(m_ins, "DB_NAME", db_file)
    monkeypatch.setattr(m_prof, "DB_NAME", db_file)

    import database.init_db as db_mod
    import services.inscripcion_service as ins_svc  # ← nuevo

    def _get_conn():
        c = sqlite3.connect(db_file)
        c.execute("PRAGMA foreign_keys = ON")
        return c

    monkeypatch.setattr(db_mod, "get_connection", _get_conn)
    monkeypatch.setattr(ins_svc, "get_connection", _get_conn)  # ← nuevo

    return db_file

@pytest.fixture()
def app_client(db_path, monkeypatch):
    from app import app

    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# 1. PRUEBAS UNITARIAS — simulacion_service.py

class TestModelo:
    """Pruebas de la función diferencial dy/dt = k*(5 - y)"""

    def test_retorna_cero_cuando_y_igual_a_5(self):
        assert modelo(5, 0.05) == 0.0

    def test_retorna_positivo_cuando_y_menor_a_5(self):
        assert modelo(3.0, 0.05) > 0

    def test_retorna_negativo_cuando_y_mayor_a_5(self):
        assert modelo(5.5, 0.05) < 0

    def test_crece_mas_rapido_con_k_mayor(self):
        assert modelo(3.0, 0.1) > modelo(3.0, 0.05)


class TestDeterminarIteraciones:

    def test_nota_muy_alta_pocas_iteraciones(self):
        assert determinar_iteraciones(4.8) == 10

    def test_nota_media_iteraciones_moderadas(self):
        assert determinar_iteraciones(3.5) == 30

    def test_nota_baja_muchas_iteraciones(self):
        assert determinar_iteraciones(1.5) == 70

    def test_nota_limite_exacto_2_0(self):
        assert determinar_iteraciones(2.0) == 60

    def test_nota_limite_exacto_3_0(self):
        assert determinar_iteraciones(3.0) == 45

    def test_iteraciones_mayores_para_notas_menores(self):
        assert determinar_iteraciones(2.0) > determinar_iteraciones(3.0)
        assert determinar_iteraciones(3.0) > determinar_iteraciones(4.0)


class TestDeterminarK:

    def test_nota_alta_k_pequeno(self):
        assert determinar_k(4.5) == 0.03

    def test_nota_media_k_medio(self):
        assert determinar_k(3.5) == 0.045

    def test_nota_baja_k_grande(self):
        assert determinar_k(2.5) == 0.06

    def test_limite_exacto_3_0(self):
        assert determinar_k(3.0) == 0.045

    def test_limite_exacto_4_0(self):
        assert determinar_k(4.0) == 0.03


class TestSimularMejora:
    """Pruebas de integración del algoritmo RK4 completo."""

    def test_retorna_estructura_correcta(self):
        resultado = simular_mejora(3.0)
        assert "nota_inicial" in resultado
        assert "nota_final_estimada" in resultado
        assert "iteraciones" in resultado
        assert "historial" in resultado

    def test_nota_final_mayor_que_inicial(self):
        resultado = simular_mejora(3.0)
        assert resultado["nota_final_estimada"] > resultado["nota_inicial"]

    def test_nota_final_no_supera_5(self):
        resultado = simular_mejora(1.0)
        assert resultado["nota_final_estimada"] <= 5.0

    def test_nota_inicial_5_no_cambia(self):
        """Con y=5 el modelo retorna 0, no debe haber cambio."""
        resultado = simular_mejora(5.0)
        assert abs(resultado["nota_final_estimada"] - 5.0) < 0.01

    def test_historial_longitud_correcta(self):
        resultado = simular_mejora(3.0)
        # historial incluye el valor inicial + una entrada por iteración
        assert len(resultado["historial"]) == resultado["iteraciones"] + 1

    def test_historial_primer_valor_es_nota_inicial(self):
        resultado = simular_mejora(2.5)
        assert resultado["historial"][0] == 2.5

    def test_historial_es_monotono_creciente(self):
        resultado = simular_mejora(3.0)
        for i in range(1, len(resultado["historial"])):
            assert resultado["historial"][i] >= resultado["historial"][i - 1]

    def test_nota_muy_baja_mejora_significativamente(self):
        resultado = simular_mejora(1.0)
        assert resultado["nota_final_estimada"] > 2.0

    @pytest.mark.parametrize("nota", [1.0, 2.0, 3.0, 3.5, 4.0, 4.5, 4.9])
    def test_siempre_mejora_para_cualquier_nota_valida(self, nota):
        resultado = simular_mejora(nota)
        assert resultado["nota_final_estimada"] >= nota

# 2. PRUEBAS DE INTEGRACIÓN — Endpoints Flask

class TestEstudiantes:

    def test_crear_estudiante_exitoso(self, app_client):
        rv = app_client.post("/estudiantes", json={
            "nombre": "Ana",
            "apellido": "López",
            "documento": "123456",
            "carrera": "Ingeniería de Sistemas"
        })
        assert rv.status_code == 201

    def test_crear_estudiante_faltan_datos(self, app_client):
        rv = app_client.post("/estudiantes", json={"nombre": "Ana"})
        assert rv.status_code == 400

    def test_crear_estudiante_documento_duplicado(self, app_client):
        payload = {
            "nombre": "Ana", "apellido": "López",
            "documento": "999", "carrera": "Sistemas"
        }
        app_client.post("/estudiantes", json=payload)
        rv = app_client.post("/estudiantes", json=payload)
        assert rv.status_code in (400, 409)

    def test_listar_estudiantes_vacia(self, app_client):
        rv = app_client.get("/estudiantes")
        assert rv.status_code == 200
        assert rv.get_json() == []

    def test_listar_estudiantes_con_datos(self, app_client):
        app_client.post("/estudiantes", json={
            "nombre": "Carlos", "apellido": "Ruiz",
            "documento": "111", "carrera": "Sistemas"
        })
        rv = app_client.get("/estudiantes")
        assert rv.status_code == 200
        assert len(rv.get_json()) == 1

    def test_obtener_estudiante_por_id(self, app_client):
        app_client.post("/estudiantes", json={
            "nombre": "María", "apellido": "Gómez",
            "documento": "222", "carrera": "Sistemas"
        })
        rv = app_client.get("/estudiantes/1")
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["nombre"] == "María"

    def test_obtener_estudiante_inexistente(self, app_client):
        rv = app_client.get("/estudiantes/999")
        assert rv.status_code == 404

    def test_eliminar_estudiante(self, app_client):
        app_client.post("/estudiantes", json={
            "nombre": "Luis", "apellido": "Pérez",
            "documento": "333", "carrera": "Sistemas"
        })
        rv = app_client.delete("/estudiantes/1")
        assert rv.status_code == 200

    def test_eliminar_estudiante_inexistente(self, app_client):
        rv = app_client.delete("/estudiantes/999")
        assert rv.status_code == 404

class TestProfesores:

    def test_crear_profesor_exitoso(self, app_client):
        rv = app_client.post("/profesores", json={
            "nombre": "Jorge", "apellido": "Martínez"
        })
        assert rv.status_code == 201

    def test_crear_profesor_faltan_datos(self, app_client):
        rv = app_client.post("/profesores", json={"nombre": "Jorge"})
        assert rv.status_code == 400

    def test_listar_profesores(self, app_client):
        app_client.post("/profesores", json={"nombre": "Jorge", "apellido": "Martínez"})
        rv = app_client.get("/profesores")
        assert rv.status_code == 200
        assert len(rv.get_json()) >= 1

class TestMaterias:

    def test_listar_materias_con_datos_iniciales(self, app_client):
        rv = app_client.get("/materias")
        assert rv.status_code == 200
        assert len(rv.get_json()) >= 3  # las 3 del SCHEMA de prueba

    def test_crear_materia_exitosa(self, app_client):
        rv = app_client.post("/materias", json={
            "nombre": "Calidad de Software",
            "carrera": "Ingeniería de Sistemas"
        })
        assert rv.status_code == 201

    def test_crear_materia_faltan_datos(self, app_client):
        rv = app_client.post("/materias", json={"nombre": "Calidad de Software"})
        assert rv.status_code == 400

class TestInscripciones:

    def _crear_estudiante(self, client, doc="001"):
        client.post("/estudiantes", json={
            "nombre": "Test", "apellido": "User",
            "documento": doc, "carrera": "Sistemas"
        })

    def test_inscripcion_exitosa(self, app_client):
        self._crear_estudiante(app_client)
        rv = app_client.post("/inscripciones", json={
            "estudiante_id": 1, "materia_id": 1
        })
        assert rv.status_code == 201

    def test_inscripcion_duplicada(self, app_client):
        self._crear_estudiante(app_client)
        app_client.post("/inscripciones", json={"estudiante_id": 1, "materia_id": 1})
        rv = app_client.post("/inscripciones", json={"estudiante_id": 1, "materia_id": 1})
        assert rv.status_code == 400

    def test_inscripcion_estudiante_inexistente(self, app_client):
        rv = app_client.post("/inscripciones", json={
            "estudiante_id": 999, "materia_id": 1
        })
        assert rv.status_code == 404

    def test_inscripcion_materia_inexistente(self, app_client):
        self._crear_estudiante(app_client)
        rv = app_client.post("/inscripciones", json={
            "estudiante_id": 1, "materia_id": 999
        })
        assert rv.status_code == 404

    def test_inscripcion_faltan_datos(self, app_client):
        rv = app_client.post("/inscripciones", json={"estudiante_id": 1})
        assert rv.status_code == 400

    def test_listar_inscripciones(self, app_client):
        self._crear_estudiante(app_client)
        app_client.post("/inscripciones", json={"estudiante_id": 1, "materia_id": 1})
        rv = app_client.get("/inscripciones")
        assert rv.status_code == 200
        data = rv.get_json()
        assert len(data) == 1
        assert "estudiante" in data[0]
        assert "materia" in data[0]

    def test_actualizar_nota_corte1(self, app_client):
        self._crear_estudiante(app_client)
        app_client.post("/inscripciones", json={"estudiante_id": 1, "materia_id": 1})
        rv = app_client.put("/inscripciones/1/notas", json={"nota_corte1": 3.5})
        assert rv.status_code == 200

    def test_actualizar_nota_inscripcion_inexistente(self, app_client):
        rv = app_client.put("/inscripciones/999/notas", json={"nota_corte1": 3.5})
        assert rv.status_code == 404

class TestSimulacionEndpoint:

    def test_simular_mejora_exitoso(self, app_client):
        rv = app_client.post("/simular-mejora", json={"nota_corte1": 3.0})
        assert rv.status_code == 200
        data = rv.get_json()
        assert "nota_final_estimada" in data
        assert "historial" in data

    def test_simular_sin_nota(self, app_client):
        rv = app_client.post("/simular-mejora", json={})
        assert rv.status_code == 400

    def test_simular_nota_limite_inferior(self, app_client):
        rv = app_client.post("/simular-mejora", json={"nota_corte1": 0.0})
        assert rv.status_code == 200

    def test_simular_nota_perfecta(self, app_client):
        rv = app_client.post("/simular-mejora", json={"nota_corte1": 5.0})
        assert rv.status_code == 200
        data = rv.get_json()
        assert abs(data["nota_final_estimada"] - 5.0) < 0.01

class TestProyeccion:

    def _setup_inscripcion_con_nota(self, client):
        client.post("/estudiantes", json={
            "nombre": "Test", "apellido": "User",
            "documento": "001", "carrera": "Sistemas"
        })
        client.post("/inscripciones", json={"estudiante_id": 1, "materia_id": 1})
        client.put("/inscripciones/1/notas", json={"nota_corte1": 3.2})

    def test_proyeccion_exitosa(self, app_client):
        self._setup_inscripcion_con_nota(app_client)
        rv = app_client.get("/proyeccion/1")
        assert rv.status_code == 200
        data = rv.get_json()
        assert "nota_final_estimada" in data
        assert "historial" in data

    def test_proyeccion_inscripcion_inexistente(self, app_client):
        rv = app_client.get("/proyeccion/999")
        assert rv.status_code == 404

    def test_proyeccion_sin_nota_registrada(self, app_client):
        app_client.post("/estudiantes", json={
            "nombre": "Test", "apellido": "User",
            "documento": "001", "carrera": "Sistemas"
        })
        app_client.post("/inscripciones", json={"estudiante_id": 1, "materia_id": 1})
        # nota_corte1 queda en 0 (DEFAULT), lo cual sí permite simular
        rv = app_client.get("/proyeccion/1")
        assert rv.status_code in (200, 400)