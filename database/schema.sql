CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    documento TEXT NOT NULL UNIQUE,
    carrera TEXT NOT NULL,
    semestre INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS profesores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS materias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    carrera TEXT NOT NULL,
    semestre INTEGER NOT NULL
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

INSERT INTO materias (nombre, carrera, semestre) VALUES
('Cálculo Diferencial','Ingeniería de Sistemas',1),
('Física Mecánica','Ingeniería de Sistemas',1),
('Introducción a la Ingeniería','Ingeniería de Sistemas',1),
('Lógica y Algoritmos','Ingeniería de Sistemas',1),
('Lógica Matemática','Ingeniería de Sistemas',1),
('Competencias de Comunicación','Ingeniería de Sistemas',1),
('Cátedra Unilibrista','Ingeniería de Sistemas',1),
('Cálculo Integral','Ingeniería de Sistemas',2),
('Electricidad y Magnetismo','Ingeniería de Sistemas',2),
('Álgebra Lineal','Ingeniería de Sistemas',2),
('Pensamiento Sistémico','Ingeniería de Sistemas',2),
('Fundamentos de programación','Ingeniería de Sistemas',2),
('Electrónica Digital','Ingeniería de Sistemas',2),
('Cálculo Multivariado y Vectorial','Ingeniería de Sistemas',3),
('Probabilidad y Estadística','Ingeniería de Sistemas',3),
('Diseño en Ingeniería','Ingeniería de Sistemas',3),
('Estructuras de Datos','Ingeniería de Sistemas',3),
('Arquitectura de Computadores','Ingeniería de Sistemas',3),
('Ingeniería de Software I','Ingeniería de Sistemas',3),
('Ecuaciones Diferenciales','Ingeniería de Sistemas',4),
('Catedra de Sostenibilidad','Ingeniería de Sistemas',4),
('Constitución Política','Ingeniería de Sistemas',4),
('Fundamentos de base de datos','Ingeniería de Sistemas',4),
('Programación I','Ingeniería de Sistemas',4),
('Ingeniería de Software II','Ingeniería de Sistemas',4),
('Matemáticas Discretas','Ingeniería de Sistemas',5),
('Sistemas Operativos','Ingeniería de Sistemas',5),
('Sistemas de base de datos','Ingeniería de Sistemas',5),
('Fundamentos de Economía','Ingeniería de Sistemas',5),
('Ingeniería de Software III','Ingeniería de Sistemas',5),
('Programación II','Ingeniería de Sistemas',5),
('Formulación y Evaluación de Proyectos','Ingeniería de Sistemas',6),
('Programación Web','Ingeniería de Sistemas',6),
('Programación Lineal','Ingeniería de Sistemas',6),
('Arquitectura de Información','Ingeniería de Sistemas',6),
('Redes de Computadores','Ingeniería de Sistemas',6),
('Metodología de la Investigación','Ingeniería de Sistemas',7),
('Ética','Ingeniería de Sistemas',7),
('Seguridad de la Información','Ingeniería de Sistemas',7),
('Inteligencia Artificial','Ingeniería de Sistemas',7),
('Programación Móvil','Ingeniería de Sistemas',7),
('Gestión de Proyectos de Ingeniería','Ingeniería de Sistemas',7),
('Ingeniería Aplicada','Ingeniería de Sistemas',8),
('Arquitectura Empresarial','Ingeniería de Sistemas',8),
('Sistemas Integrados de Gestión','Ingeniería de Sistemas',8),
('Gerencia Estratégica','Ingeniería de Sistemas',8)