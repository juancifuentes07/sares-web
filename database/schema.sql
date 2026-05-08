CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    documento TEXT NOT NULL UNIQUE,
    carrera TEXT NOT NULL,
);

CREATE TABLE IF NOT EXISTS profesores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS materias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
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

INSERT OR IGNORE INTO materias (nombre, carrera) VALUES
('Cálculo Diferencial','Ingeniería de Sistemas'),
('Física Mecánica','Ingeniería de Sistemas'),   
('Introducción a la Ingeniería','Ingeniería de Sistemas'),
('Lógica y Algoritmos','Ingeniería de Sistemas'),
('Lógica Matemática','Ingeniería de Sistemas'),
('Competencias de Comunicación','Ingeniería de Sistemas'),
('Cátedra Unilibrista','Ingeniería de Sistemas'),
('Cálculo Integral','Ingeniería de Sistemas'),
('Electricidad y Magnetismo','Ingeniería de Sistemas'),
('Álgebra Lineal','Ingeniería de Sistemas'),
('Pensamiento Sistémico','Ingeniería de Sistemas'),
('Fundamentos de programación','Ingeniería de Sistemas'),
('Electrónica Digital','Ingeniería de Sistemas'),
('Cálculo Multivariado y Vectorial','Ingeniería de Sistemas'),
('Probabilidad y Estadística','Ingeniería de Sistemas'),
('Diseño en Ingeniería','Ingeniería de Sistemas'),
('Estructuras de Datos','Ingeniería de Sistemas'),
('Arquitectura de Computadores','Ingeniería de Sistemas'),
('Ingeniería de Software I','Ingeniería de Sistemas'),
('Ecuaciones Diferenciales','Ingeniería de Sistemas'),
('Catedra de Sostenibilidad','Ingeniería de Sistemas'),
('Constitución Política','Ingeniería de Sistemas'),
('Fundamentos de base de datos','Ingeniería de Sistemas'),
('Programación I','Ingeniería de Sistemas'),
('Ingeniería de Software II','Ingeniería de Sistemas'),
('Matemáticas Discretas','Ingeniería de Sistemas'),
('Sistemas Operativos','Ingeniería de Sistemas'),
('Sistemas de base de datos','Ingeniería de Sistemas'),
('Fundamentos de Economía','Ingeniería de Sistemas'),
('Ingeniería de Software III','Ingeniería de Sistemas'),
('Programación II','Ingeniería de Sistemas'),
('Formulación y Evaluación de Proyectos','Ingeniería de Sistemas'),
('Programación Web','Ingeniería de Sistemas'),
('Programación Lineal','Ingeniería de Sistemas'),
('Arquitectura de Información','Ingeniería de Sistemas'),
('Redes de Computadores','Ingeniería de Sistemas'),
('Metodología de la Investigación','Ingeniería de Sistemas'),
('Ética','Ingeniería de Sistemas'),
('Seguridad de la Información','Ingeniería de Sistemas'),
('Inteligencia Artificial','Ingeniería de Sistemas'),
('Programación Móvil','Ingeniería de Sistemas'),
('Gestión de Proyectos de Ingeniería','Ingeniería de Sistemas'),
('Ingeniería Aplicada','Ingeniería de Sistemas'),
('Arquitectura Empresarial','Ingeniería de Sistemas'),
('Sistemas Integrados de Gestión','Ingeniería de Sistemas'),
('Gerencia Estratégica','Ingeniería de Sistemas')