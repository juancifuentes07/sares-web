-- Crear Tablas
CREATE TABLE estudiantes (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    apellido VARCHAR2(100) NOT NULL,
    documento VARCHAR2(50) NOT NULL UNIQUE,
    carrera VARCHAR2(100) NOT NULL
);

CREATE TABLE profesores (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    apellido VARCHAR2(100) NOT NULL
);

CREATE TABLE materias (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR2(150) NOT NULL UNIQUE,
    carrera VARCHAR2(100) NOT NULL
);

CREATE TABLE inscripciones (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    estudiante_id NUMBER NOT NULL,
    materia_id NUMBER NOT NULL,
    nota_corte1 NUMBER(3,2) DEFAULT 0,
    CONSTRAINT fk_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    CONSTRAINT fk_materia FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE,
    CONSTRAINT uq_est_mat UNIQUE(estudiante_id, materia_id)
);

INSERT INTO materias (nombre, carrera) VALUES ('Cálculo Diferencial','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Física Mecánica','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Introducción a la Ingeniería','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Lógica y Algoritmos','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Lógica Matemática','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Competencias de Comunicación','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Cátedra Unilibrista','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Cálculo Integral','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Electricidad y Magnetismo','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Álgebra Lineal','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Pensamiento Sistémico','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Fundamentos de programación','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Electrónica Digital','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Cálculo Multivariado y Vectorial','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Probabilidad y Estadística','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Diseño en Ingeniería','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Estructuras de Datos','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Arquitectura de Computadores','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Ingeniería de Software I','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Ecuaciones Diferenciales','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Catedra de Sostenibilidad','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Constitución Política','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Fundamentos de base de datos','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Programación I','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Ingeniería de Software II','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Matemáticas Discretas','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Sistemas Operativos','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Sistemas de base de datos','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Fundamentos de Economía','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Ingeniería de Software III','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Programación II','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Formulación y Evaluación de Proyectos','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Programación Web','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Programación Lineal','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Arquitectura de Información','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Redes de Computadores','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Metodología de la Investigación','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Ética','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Seguridad de la Información','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Inteligencia Artificial','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Programación Móvil','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Gestión de Proyectos de Ingeniería','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Ingeniería Aplicada','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Arquitectura Empresarial','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Sistemas Integrados de Gestión','Ingeniería de Sistemas');
INSERT INTO materias (nombre, carrera) VALUES ('Gerencia Estratégica','Ingeniería de Sistemas');

COMMIT;

SELECT COUNT(*) FROM materias;