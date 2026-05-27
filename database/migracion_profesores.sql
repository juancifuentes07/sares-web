-- ============================================================
-- SARES - Migración: módulo de profesores y seguimiento académico
-- ============================================================
-- Ejecutar UNA vez en Oracle (SQL Developer / SQL*Plus), conectado
-- al mismo usuario que usa la aplicación.
--
-- Agrega lo necesario para:
--   - que cada profesor tenga documento y materias en que es experto
--   - asignar automáticamente un profesor a un estudiante en riesgo
-- ============================================================


-- ------------------------------------------------------------
-- 1. Agregar la columna 'documento' a la tabla profesores
-- ------------------------------------------------------------
-- La tabla profesores ya existe (con nombre y apellido). Solo se
-- le agrega la columna documento. Se agrega como NULL para no
-- chocar con filas existentes; el script de carga la rellena.
-- ------------------------------------------------------------
ALTER TABLE profesores ADD (documento VARCHAR2(50));


-- ------------------------------------------------------------
-- 2. Relación muchos-a-muchos profesor <-> materia
--    Un profesor es experto en varias materias;
--    cada materia tiene al menos dos profesores.
-- ------------------------------------------------------------
CREATE TABLE profesor_materia (
    profesor_id NUMBER NOT NULL,
    materia_id NUMBER NOT NULL,
    CONSTRAINT pk_prof_mat PRIMARY KEY (profesor_id, materia_id),
    CONSTRAINT fk_pm_profesor FOREIGN KEY (profesor_id) REFERENCES profesores(id) ON DELETE CASCADE,
    CONSTRAINT fk_pm_materia FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
);


-- ------------------------------------------------------------
-- 3. Seguimiento académico
--    Cuando un estudiante entra en riesgo en una materia, se le
--    asigna un profesor experto que sigue su proceso de mejora.
--    estado: 'en_seguimiento' | 'mejorado' | 'cerrado'
-- ------------------------------------------------------------
CREATE TABLE seguimientos (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    inscripcion_id NUMBER NOT NULL UNIQUE,
    profesor_id NUMBER NOT NULL,
    estado VARCHAR2(20) DEFAULT 'en_seguimiento' NOT NULL,
    nota_inicial NUMBER(3,2),
    fecha_asignacion DATE DEFAULT SYSDATE NOT NULL,
    observaciones VARCHAR2(1000) DEFAULT '',
    CONSTRAINT fk_seg_inscripcion FOREIGN KEY (inscripcion_id) REFERENCES inscripciones(id) ON DELETE CASCADE,
    CONSTRAINT fk_seg_profesor FOREIGN KEY (profesor_id) REFERENCES profesores(id) ON DELETE CASCADE
);


-- ------------------------------------------------------------
-- 4. Tareas / actividades que el profesor asigna al estudiante
--    Son las actividades que el estudiante debe realizar para
--    mejorar su rendimiento (talleres, repasos, ejercicios).
--    estado: 'por_hacer' | 'hecha'
-- ------------------------------------------------------------
CREATE TABLE tareas (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    seguimiento_id NUMBER NOT NULL,
    descripcion VARCHAR2(300) NOT NULL,
    estado VARCHAR2(20) DEFAULT 'por_hacer' NOT NULL,
    fecha_creacion DATE DEFAULT SYSDATE NOT NULL,
    CONSTRAINT fk_tarea_seg FOREIGN KEY (seguimiento_id) REFERENCES seguimientos(id) ON DELETE CASCADE
);

COMMIT;
