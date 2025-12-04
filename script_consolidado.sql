------------------------------------------------ 
-- SISTEMA DE AUTOMATIZACIÓN PARA SEGUIMIENTO DE EGRESADOS
-- Script Consolidado de Base de Datos PostgreSQL
-- Incluye: Limpieza, Estructura, Datos Maestros y Datos de Ejemplo
------------------------------------------------ 

-- =====================================================
-- PASO 1: LIMPIAR BASE DE DATOS (OPCIONAL)
-- =====================================================

-- Descomentar las siguientes líneas si necesitas limpiar la base de datos
-- DROP TABLE IF EXISTS evaluacion_formacion CASCADE;
-- DROP TABLE IF EXISTS encuesta_egresado CASCADE;
-- DROP TABLE IF EXISTS certificacion CASCADE;
-- DROP TABLE IF EXISTS detalle_egresado CASCADE;
-- DROP TABLE IF EXISTS empresa CASCADE;
-- DROP TABLE IF EXISTS usuarios CASCADE;
-- DROP TABLE IF EXISTS egresado CASCADE;
-- DROP TABLE IF EXISTS estado_civil CASCADE;
-- DROP TABLE IF EXISTS actividad_economica CASCADE;
-- DROP TABLE IF EXISTS carrera_profesional CASCADE;

-- =====================================================
-- PASO 2: CREAR ESTRUCTURA DE TABLAS
-- =====================================================

-- =====================================================
-- TABLAS MAESTRAS
-- =====================================================

-- 1. TABLA MAESTRA: ESTADO_CIVIL (Catálogo)
CREATE TABLE estado_civil (
    id_estado SERIAL PRIMARY KEY,
    descripcion VARCHAR(50) UNIQUE NOT NULL,
    estado CHAR(1) DEFAULT 'A' CHECK (estado IN ('A', 'I'))
);

-- 2. TABLA MAESTRA: CARRERA_PROFESIONAL (Catálogo)
CREATE TABLE carrera_profesional (
    id_carrera SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    estado CHAR(1) DEFAULT 'A' CHECK (estado IN ('A', 'I'))
);

-- 3. TABLA MAESTRA: ACTIVIDAD_ECONOMICA (Catálogo)
CREATE TABLE actividad_economica (
    id_actividad SERIAL PRIMARY KEY,
    nombre VARCHAR(150) UNIQUE NOT NULL,
    codigo VARCHAR(10),
    estado CHAR(1) DEFAULT 'A' CHECK (estado IN ('A', 'I'))
);

-- 4. TABLA MAESTRA: EMPRESA
CREATE TABLE empresa (
    id_empresa SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    ruc CHAR(11) NOT NULL UNIQUE,
    direccion VARCHAR(200),
    telefono VARCHAR(15),
    correo VARCHAR(120),
    estado CHAR(1) DEFAULT 'A' CHECK (estado IN ('A', 'I'))
);

-- 5. TABLA MAESTRA: EGRESADO (Mejorada con campos del formulario)
CREATE TABLE EGRESADO (
    CODIGO              VARCHAR(20) PRIMARY KEY,
    NOMBRE              VARCHAR(100) NOT NULL,
    APELLIDOS           VARCHAR(100) NOT NULL,
    DNI                 CHAR(8) NOT NULL UNIQUE,
    FECHA_NACIMIENTO    DATE,
    SEXO                CHAR(1) CHECK (SEXO IN ('F', 'M')),
    DIRECCION           VARCHAR(200),
    TELEFONO            VARCHAR(15),
    TELEFONO_REFERENCIA VARCHAR(15),
    CORREO              VARCHAR(120) NOT NULL UNIQUE,
    ES_CONVIVIENTE      BOOLEAN DEFAULT FALSE,
    ESTADO_CIVIL_ID     INT,
    CANTIDAD_HIJOS      INT DEFAULT 0,
    TIENE_DISCAPACIDAD  BOOLEAN DEFAULT FALSE,
    CARRERA_ID          INT,
    ANIO_INGRESO        INT,
    ANIO_EGRESO         INT,
    ES_TITULADO         BOOLEAN DEFAULT FALSE,
    ANIO_TITULACION     INT,
    ESTADO              CHAR(1) NOT NULL CHECK (ESTADO IN ('A', 'I')) DEFAULT 'A',
    CONSTRAINT fk_egresado_estado_civil FOREIGN KEY (ESTADO_CIVIL_ID) REFERENCES estado_civil(id_estado),
    CONSTRAINT fk_egresado_carrera FOREIGN KEY (CARRERA_ID) REFERENCES carrera_profesional(id_carrera)
);

-- =====================================================
-- TABLAS TRANSACCIONALES
-- =====================================================

-- 1. TABLA TRANSACCIONAL: DETALLE_EGRESADO
CREATE TABLE detalle_egresado (
    ID_DETALLE           SERIAL PRIMARY KEY,
    CODIGO_EGRESADO      VARCHAR(20) NOT NULL,
    FECHA_EGRESO         DATE,
    EMPRESA_ACTUAL       VARCHAR(100),
    CARGO_ACTUAL         VARCHAR(100),
    PAIS_RESIDENCIA      VARCHAR(50),
    CIUDAD_RESIDENCIA    VARCHAR(50),
    FECHA_INCORPORACION  DATE,
    AREA_TRABAJO         VARCHAR(50),
    SUELDO_ACTUAL        DECIMAL(10, 2),
    ESTADO               CHAR(1) NOT NULL CHECK (ESTADO IN ('A', 'I')) DEFAULT 'A',
    CONSTRAINT fk_detalle_egresado FOREIGN KEY (CODIGO_EGRESADO) REFERENCES EGRESADO(CODIGO)
);

-- 2. TABLA TRANSACCIONAL: CERTIFICACION
CREATE TABLE certificacion (
    id_certificacion SERIAL PRIMARY KEY,
    codigo_egresado VARCHAR(20) NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    institucion VARCHAR(150) NOT NULL,
    fecha_obtencion DATE NOT NULL,
    archivo VARCHAR(255),
    estado CHAR(1) DEFAULT 'A' CHECK (estado IN ('A', 'I')),
    CONSTRAINT fk_certificacion_egresado FOREIGN KEY (codigo_egresado) REFERENCES EGRESADO(CODIGO)
);

-- 3. TABLA TRANSACCIONAL: ENCUESTA_EGRESADO (Basada en formulario)
CREATE TABLE encuesta_egresado (
    id_encuesta SERIAL PRIMARY KEY,
    codigo_egresado VARCHAR(20) NOT NULL,
    fecha_aplicacion DATE NOT NULL,
    
    -- SITUACIÓN LABORAL
    trabaja_actualmente BOOLEAN,
    tipo_contrato VARCHAR(50), -- 'Contrato de trabajo', 'Recibo por honorario', 'Ninguna'
    tipo_empleo VARCHAR(50), -- 'Institución pública', 'Empresa privada', 'Independiente'
    ingreso_mensual VARCHAR(50), -- Rangos de ingreso
    area_trabajo VARCHAR(100),
    actividad_economica_id INT,
    relacion_carrera VARCHAR(50), -- 'Directamente', 'Indirectamente', 'Nada relacionado'
    
    -- BÚSQUEDA DE EMPLEO
    medios_busqueda VARCHAR(255), -- Múltiples opciones separadas por comas
    cantidad_empleos_ultimo_ano INT DEFAULT 0,
    cantidad_empleos_carrera INT DEFAULT 0,
    
    -- EMPRESA ACTUAL
    nombre_empresa_actual VARCHAR(150),
    nombre_jefe_inmediato VARCHAR(100),
    telefono_empresa VARCHAR(15),
    pagina_web_empresa VARCHAR(200),
    correo_empresa VARCHAR(120),
    
    -- TRABAJO INDEPENDIENTE
    tiene_negocio BOOLEAN DEFAULT FALSE,
    cantidad_trabajadores VARCHAR(50), -- Rangos de trabajadores
    tipo_constituccion VARCHAR(50), -- 'Persona natural con RUC', 'EIRL', 'SRL', etc.
    actividad_economica_negocio_id INT,
    
    estado CHAR(1) DEFAULT 'A' CHECK (estado IN ('A', 'I')),
    
    CONSTRAINT fk_encuesta_egresado FOREIGN KEY (codigo_egresado) REFERENCES EGRESADO(CODIGO),
    CONSTRAINT fk_encuesta_actividad FOREIGN KEY (actividad_economica_id) REFERENCES actividad_economica(id_actividad),
    CONSTRAINT fk_encuesta_actividad_negocio FOREIGN KEY (actividad_economica_negocio_id) REFERENCES actividad_economica(id_actividad)
);

-- 4. TABLA TRANSACCIONAL: EVALUACION_FORMACION (Evaluación de formación)
CREATE TABLE evaluacion_formacion (
    id_evaluacion SERIAL PRIMARY KEY,
    id_encuesta INT NOT NULL,
    
    -- EVALUACIÓN DE LA FORMACIÓN
    formacion_util BOOLEAN,
    logros VARCHAR(500), -- Múltiples logros separados por comas
    competencias_destacadas VARCHAR(500), -- Múltiples competencias separadas por comas
    mejor_preparado BOOLEAN,
    razones_mejor_preparado VARCHAR(500), -- Múltiples razones separadas por comas
    
    -- ASPECTOS A MEJORAR
    aspectos_mejorar VARCHAR(500), -- Múltiples aspectos separados por comas
    
    -- SATISFACCIÓN
    satisfecho_formacion BOOLEAN,
    motivos_satisfaccion VARCHAR(500), -- Múltiples motivos separados por comas
    motivos_insatisfaccion VARCHAR(500), -- Múltiples motivos separados por comas
    
    -- RECONOCIMIENTOS
    tiene_reconocimiento BOOLEAN DEFAULT FALSE,
    detalle_reconocimiento TEXT,
    
    -- RECOMENDACIÓN
    recomendaria_carrera BOOLEAN,
    sugerencias TEXT,
    
    estado CHAR(1) DEFAULT 'A' CHECK (estado IN ('A', 'I')),
    
    CONSTRAINT fk_evaluacion_encuesta FOREIGN KEY (id_encuesta) REFERENCES encuesta_egresado(id_encuesta)
);

-- =====================================================
-- PASO 3: INSERTAR DATOS MAESTROS BÁSICOS
-- =====================================================

-- Insertar estados civiles
INSERT INTO estado_civil (descripcion) VALUES 
('Soltero'), ('Casado'), ('Divorciado'), ('Viudo');

-- Insertar carreras profesionales
INSERT INTO carrera_profesional (nombre, codigo) VALUES 
('Producción Agraria', 'PA'),
('Análisis de Sistemas', 'AS');

-- Insertar actividades económicas
INSERT INTO actividad_economica (nombre) VALUES 
('Administración Pública'),
('Seguridad de Afiliación Obligatoria'),
('Reparación de Automotores, Motocicletas'),
('Agricultura, Ganadería, Caza y Silvicultura'),
('Explotación de Minas e Hidrocarburos'),
('Industrias Manufactureras'),
('Suministro de Electricidad, Gas y Agua'),
('Construcción'),
('Organización No Gubernamental (ONG)'),
('Actividades Inmobiliarias de Alquiler y Empresariales'),
('Transporte, Almacenamiento y Comunicaciones'),
('Servicios Sociales y de Salud'),
('Hoteles y Restaurantes'),
('Finanzas'),
('Educación'),
('Servicio doméstico'),
('Defensa'),
('Comercio'),
('Servicios');

-- Insertar empresas de ejemplo
INSERT INTO empresa (nombre, ruc, direccion, telefono, correo)
VALUES ('TecnoSoft Perú S.A.C.', '20458796123', 'Av. Javier Prado 1234, San Isidro, Lima', '(01) 654-7890', 'contacto@tecnosoft.com.pe');

INSERT INTO empresa (nombre, ruc, direccion, telefono, correo)
VALUES ('InovaTech Solutions EIRL', '20678945211', 'Calle Los Álamos 567, Miraflores, Lima', '(01) 768-4562', 'soporte@innovatech.com');

-- =====================================================
-- PASO 4: INSERTAR EGRESADOS DE EJEMPLO
-- =====================================================

INSERT INTO EGRESADO (
    CODIGO, NOMBRE, APELLIDOS, DNI, FECHA_NACIMIENTO, SEXO, DIRECCION, 
    TELEFONO, CORREO, ES_CONVIVIENTE, ESTADO_CIVIL_ID, CANTIDAD_HIJOS, 
    CARRERA_ID, ANIO_INGRESO, ANIO_EGRESO, ES_TITULADO, ANIO_TITULACION, ESTADO
) VALUES 
('EG001', 'María', 'Pérez Gómez', '12345678', '1995-03-15'::DATE, 'F', 
 'Av. Principal 123, Lima', '987654321', 'maria.perez@example.com', 
 FALSE, 1, 0, 2, 2020, 2023, TRUE, 2024, 'A'),

('EG002', 'Luis', 'Ramírez Soto', '87654321', '1993-07-22'::DATE, 'M', 
 'Jr. Libertad 456, Arequipa', '912345678', 'luis.ramirez@example.com', 
 TRUE, 2, 1, 1, 2019, 2022, TRUE, 2023, 'A'),

('EG003', 'Ana', 'García López', '11223344', '1994-05-10'::DATE, 'F', 
 'Calle Real 789, Trujillo', '955667788', 'ana.garcia@example.com', 
 FALSE, 1, 0, 2, 2020, 2023, TRUE, 2024, 'A'),

('EG004', 'Carlos', 'Mendoza Silva', '55667788', '1992-11-30'::DATE, 'M', 
 'Av. Grau 321, Chiclayo', '944556677', 'carlos.mendoza@example.com', 
 TRUE, 2, 2, 1, 2019, 2022, TRUE, 2023, 'A'),

('EG005', 'Patricia', 'Vega Torres', '99887766', '1996-08-15'::DATE, 'F', 
 'Jr. Unión 654, Piura', '933445566', 'patricia.vega@example.com', 
 FALSE, 1, 0, 2, 2021, 2024, FALSE, NULL, 'A'),

('EG006', 'Roberto', 'Díaz Herrera', '44332211', '1991-12-05'::DATE, 'M', 
 'Av. Bolognesi 987, Cusco', '922334455', 'roberto.diaz@example.com', 
 TRUE, 2, 1, 1, 2018, 2021, TRUE, 2022, 'A'),

('EG007', 'Lucía', 'Morales Rojas', '77889900', '1997-02-20'::DATE, 'F', 
 'Calle Lima 147, Huancayo', '911223344', 'lucia.morales@example.com', 
 FALSE, 1, 0, 2, 2021, 2024, FALSE, NULL, 'A'),

('EG008', 'Miguel', 'López Castro', '33445566', '1990-09-12'::DATE, 'M', 
 'Av. Tacna 258, Tacna', '900112233', 'miguel.lopez@example.com', 
 TRUE, 2, 3, 1, 2018, 2021, TRUE, 2022, 'A'),

('EG009', 'Carmen', 'Torres Flores', '66778899', '1995-06-25'::DATE, 'F', 
 'Jr. Ayacucho 369, Ayacucho', '899001122', 'carmen.torres@example.com', 
 FALSE, 1, 0, 2, 2020, 2023, TRUE, 2024, 'A'),

('EG010', 'Diego', 'Herrera Ramos', '22334455', '1993-04-18'::DATE, 'M', 
 'Av. Libertad 741, Iquitos', '888990011', 'diego.herrera@example.com', 
 TRUE, 2, 1, 1, 2019, 2022, TRUE, 2023, 'A');

-- =====================================================
-- PASO 5: INSERTAR DETALLES DE EGRESADOS
-- =====================================================

INSERT INTO detalle_egresado (
    CODIGO_EGRESADO, FECHA_EGRESO, EMPRESA_ACTUAL, CARGO_ACTUAL, 
    PAIS_RESIDENCIA, CIUDAD_RESIDENCIA, FECHA_INCORPORACION, AREA_TRABAJO, SUELDO_ACTUAL, ESTADO
) VALUES 
('EG001', '2023-12-15'::DATE, 'TechCorp', 'Desarrollador Full Stack', 
 'Perú', 'Lima', '2024-01-15'::DATE, 'Tecnología', 3500.00, 'A'),

('EG002', '2023-11-20'::DATE, 'AdminSolutions', 'Analista de Negocios', 
 'Perú', 'Arequipa', '2024-02-01'::DATE, 'Administración', 2800.00, 'A'),

('EG003', '2023-10-30'::DATE, 'DataSoft', 'Analista de Datos', 
 'Perú', 'Trujillo', '2024-01-10'::DATE, 'Tecnología', 3200.00, 'A'),

('EG004', '2023-09-25'::DATE, 'AgroTech', 'Supervisor de Producción', 
 'Perú', 'Chiclayo', '2023-12-01'::DATE, 'Agricultura', 2500.00, 'A'),

('EG005', '2024-06-15'::DATE, 'WebSolutions', 'Desarrollador Web', 
 'Perú', 'Piura', '2024-07-01'::DATE, 'Tecnología', 3000.00, 'A'),

('EG006', '2023-08-20'::DATE, 'FarmCorp', 'Técnico Agrícola', 
 'Perú', 'Cusco', '2023-09-15'::DATE, 'Agricultura', 2200.00, 'A'),

('EG007', '2024-05-30'::DATE, 'TechStart', 'Programador Junior', 
 'Perú', 'Huancayo', '2024-06-15'::DATE, 'Tecnología', 2800.00, 'A'),

('EG008', '2023-07-10'::DATE, 'AgroMax', 'Especialista en Cultivos', 
 'Perú', 'Tacna', '2023-08-01'::DATE, 'Agricultura', 2400.00, 'A'),

('EG009', '2023-12-01'::DATE, 'DataCorp', 'Analista de Sistemas', 
 'Perú', 'Ayacucho', '2024-01-15'::DATE, 'Tecnología', 3100.00, 'A'),

('EG010', '2023-06-15'::DATE, 'GreenFarm', 'Coordinador Agrícola', 
 'Perú', 'Iquitos', '2023-07-01'::DATE, 'Agricultura', 2300.00, 'A');

-- =====================================================
-- PASO 6: INSERTAR CERTIFICACIONES
-- =====================================================

INSERT INTO certificacion (codigo_egresado, nombre, institucion, fecha_obtencion, archivo)
VALUES 
('EG001', 'Diplomado en Data Science', 'Universidad Nacional', '2024-03-15'::DATE, 'diplomado_datascience.pdf'),
('EG002', 'Certificación en Gestión Administrativa', 'Instituto Superior', '2023-11-20'::DATE, 'cert_gestion_admin.pdf'),
('EG003', 'Especialización en Big Data', 'Universidad Privada', '2024-02-10'::DATE, 'especializacion_bigdata.pdf'),
('EG004', 'Diplomado en Agricultura Sostenible', 'Centro Agrícola', '2023-10-15'::DATE, 'diplomado_agricultura.pdf'),
('EG005', 'Certificación en Desarrollo Web', 'Academia Tech', '2024-04-20'::DATE, 'cert_desarrollo_web.pdf'),
('EG006', 'Especialización en Cultivos Andinos', 'Instituto Agrícola', '2023-09-05'::DATE, 'especializacion_cultivos.pdf'),
('EG007', 'Diplomado en Programación', 'Universidad Tecnológica', '2024-03-30'::DATE, 'diplomado_programacion.pdf'),
('EG008', 'Certificación en Manejo de Suelos', 'Centro de Investigación', '2023-08-15'::DATE, 'cert_manejo_suelos.pdf'),
('EG009', 'Especialización en Sistemas de Información', 'Instituto Superior', '2024-01-25'::DATE, 'especializacion_sistemas.pdf'),
('EG010', 'Diplomado en Agricultura Orgánica', 'Centro Ecológico', '2023-07-20'::DATE, 'diplomado_agricultura_organica.pdf');

-- =====================================================
-- PASO 7: INSERTAR ENCUESTAS DE EGRESADOS
-- =====================================================

INSERT INTO encuesta_egresado (
    codigo_egresado, fecha_aplicacion, trabaja_actualmente, tipo_contrato, 
    tipo_empleo, ingreso_mensual, area_trabajo, actividad_economica_id, 
    relacion_carrera, medios_busqueda, cantidad_empleos_ultimo_ano, 
    cantidad_empleos_carrera, nombre_empresa_actual, nombre_jefe_inmediato, 
    telefono_empresa, correo_empresa, tiene_negocio, estado
) VALUES 
('EG001', '2024-12-01'::DATE, TRUE, 'Contrato de trabajo', 
 'Empresa privada', 'Entre 3001 y 4000', 'Ingeniería y Producción', 6, 
 'Directamente', 'Linkedin,Bolsa de trabajo', 1, 1, 
 'TechCorp Solutions', 'Carlos Mendoza', '(01) 234-5678', 'carlos.mendoza@techcorp.com', 
 FALSE, 'A'),

('EG002', '2024-11-15'::DATE, TRUE, 'Contrato de trabajo', 
 'Empresa privada', 'Entre 2001 y 3000', 'Administración y Dirección', 1, 
 'Directamente', 'Bolsa de trabajo,Redes sociales', 1, 1, 
 'AdminSolutions', 'María González', '(01) 345-6789', 'maria.gonzalez@adminsolutions.com', 
 FALSE, 'A'),

('EG003', '2024-10-20'::DATE, TRUE, 'Contrato de trabajo', 
 'Empresa privada', 'Entre 3001 y 4000', 'Administración y Dirección', 14, 
 'Directamente', 'Linkedin,Bolsa de trabajo', 1, 1, 
 'DataSoft Perú', 'Roberto Silva', '(01) 456-7890', 'roberto.silva@datasoft.com', 
 FALSE, 'A'),

('EG004', '2024-09-10'::DATE, TRUE, 'Contrato de trabajo', 
 'Empresa privada', 'Entre 2001 y 3000', 'Agricultura, Ganadería, Caza y Silvicultura', 4, 
 'Directamente', 'Bolsa de trabajo', 1, 1, 
 'AgroTech Solutions', 'Patricia López', '(01) 567-8901', 'patricia.lopez@agrotech.com', 
 FALSE, 'A'),

('EG005', '2024-08-05'::DATE, TRUE, 'Contrato de trabajo', 
 'Empresa privada', 'Entre 2001 y 3000', 'Ingeniería y Producción', 6, 
 'Directamente', 'Redes sociales', 1, 1, 
 'WebSolutions', 'Luis Vega', '(01) 678-9012', 'luis.vega@websolutions.com', 
 FALSE, 'A'),

('EG006', '2024-07-15'::DATE, TRUE, 'Contrato de trabajo', 
 'Empresa privada', 'Entre 2001 y 3000', 'Agricultura, Ganadería, Caza y Silvicultura', 4, 
 'Directamente', 'Bolsa de trabajo', 1, 1, 
 'FarmCorp', 'Carmen Díaz', '(01) 789-0123', 'carmen.diaz@farmcorp.com', 
 FALSE, 'A'),

('EG007', '2024-06-20'::DATE, TRUE, 'Contrato de trabajo', 
 'Empresa privada', 'Entre 2001 y 3000', 'Ingeniería y Producción', 6, 
 'Directamente', 'Linkedin', 1, 1, 
 'TechStart', 'Diego Rojas', '(01) 890-1234', 'diego.rojas@techstart.com', 
 FALSE, 'A'),

('EG008', '2024-05-25'::DATE, TRUE, 'Contrato de trabajo', 
 'Empresa privada', 'Entre 2001 y 3000', 'Agricultura, Ganadería, Caza y Silvicultura', 4, 
 'Directamente', 'Bolsa de trabajo', 1, 1, 
 'AgroMax', 'Patricia López', '(01) 901-2345', 'patricia.lopez@agromax.com', 
 FALSE, 'A'),

('EG009', '2024-04-30'::DATE, TRUE, 'Contrato de trabajo', 
 'Empresa privada', 'Entre 3001 y 4000', 'Ingeniería y Producción', 6, 
 'Directamente', 'Linkedin,Bolsa de trabajo', 1, 1, 
 'DataCorp', 'Miguel Torres', '(01) 012-3456', 'miguel.torres@datacorp.com', 
 FALSE, 'A'),

('EG010', '2024-03-15'::DATE, TRUE, 'Contrato de trabajo', 
 'Empresa privada', 'Entre 2001 y 3000', 'Administración y Dirección', 4, 
 'Directamente', 'Bolsa de trabajo', 1, 1, 
 'GreenFarm', 'Lucía Morales', '(01) 123-4567', 'lucia.morales@greenfarm.com', 
 FALSE, 'A');

-- =====================================================
-- PASO 8: INSERTAR EVALUACIONES DE FORMACIÓN
-- =====================================================

INSERT INTO evaluacion_formacion (
    id_encuesta, formacion_util, logros, competencias_destacadas, 
    mejor_preparado, razones_mejor_preparado, aspectos_mejorar, 
    satisfecho_formacion, motivos_satisfaccion, tiene_reconocimiento, 
    recomendaria_carrera, sugerencias
) VALUES 
(1, TRUE, 'Un sueldo adecuado en función a tu experiencia personal,Desarrollo personal', 
 'Dominio de su especialidad,Capacidad del trabajo grupal,Habilidad comunicativa', 
 TRUE, 'Por el equipamiento especializado de la carrera,Por el desarrollo de los conocimientos básicos para el desempeño laboral', 
 'Actualización de los Docente,Recursos Tecnológicos', 
 TRUE, 'El equipamiento con que cuenta la carrera permite una buena formación tecnológica,La metodología de la Alternancia Educativa', 
 TRUE, TRUE, 'Mejorar la infraestructura de laboratorios y actualizar el equipamiento tecnológico'),

(2, TRUE, 'Desarrollo personal,Te ayudó en el desarrollo del plan de vida', 
 'Organización del trabajo,Capacidad del trabajo grupal,Disciplina honestidad orden', 
 TRUE, 'Por el desarrollo de los conocimientos básicos para el desempeño laboral,Porque la formación está relacionada con la práctica laboral', 
 'Actualización de los Docente,Metodología de enseñanza del Docente', 
 TRUE, 'La metodología de la Alternancia Educativa,El perfil ocupacional es actualizado y da mayores posibilidades de empleo', 
 FALSE, TRUE, 'Mejorar la metodología de enseñanza y actualizar a los docentes'),

(3, TRUE, 'Un sueldo adecuado en función a tu experiencia personal,Realizar mi empresa', 
 'Dominio de su especialidad,Capacidad creativa innovación', 
 TRUE, 'Por el equipamiento especializado de la carrera,Por el desarrollo de los conocimientos básicos para el desempeño laboral', 
 'Recursos Tecnológicos,Infraestructura', 
 TRUE, 'El equipamiento con que cuenta la carrera permite una buena formación tecnológica,Los docentes de la carrera tienen experiencia y están actualizados en la especialidad', 
 TRUE, TRUE, 'Actualizar la infraestructura y recursos tecnológicos'),

(4, TRUE, 'Desarrollo personal,Te ayudó en el desarrollo del plan de vida', 
 'Disciplina honestidad orden,Capacidad del trabajo grupal', 
 TRUE, 'Porque la formación está relacionada con la práctica laboral,Por el desarrollo de aptitudes hacia la innovación e investigación', 
 'Actualización de los Docente,Equipamiento', 
 TRUE, 'La metodología de la Alternancia Educativa,La formación y adquisición de habilidades básicas mejoran el desempeño laboral', 
 FALSE, TRUE, 'Mejorar el equipamiento y actualizar a los docentes'),

(5, TRUE, 'Un sueldo adecuado en función a tu experiencia personal,Desarrollo personal', 
 'Dominio de su especialidad,Capacidad creativa innovación', 
 TRUE, 'Por el equipamiento especializado de la carrera,Porque la formación está relacionada con la práctica laboral', 
 'Recursos Tecnológicos,Laboratorios', 
 TRUE, 'El equipamiento con que cuenta la carrera permite una buena formación tecnológica,La metodología de la Alternancia Educativa', 
 TRUE, TRUE, 'Mejorar los laboratorios y recursos tecnológicos'),

(6, TRUE, 'Realizar mi empresa,Desarrollo personal', 
 'Capacidad creativa innovación,Organización del trabajo', 
 TRUE, 'Por el desarrollo de aptitudes hacia la innovación e investigación,Porque la formación está relacionada con la práctica laboral', 
 'Metodología de enseñanza del Docente,Actualización de los Docente', 
 TRUE, 'La formación de aptitudes de autoformación y disciplina ayuda a fomentar empresas,Los docentes de la carrera tienen experiencia y están actualizados en la especialidad', 
 TRUE, TRUE, 'Mejorar la metodología de enseñanza y actualizar a los docentes'),

(7, TRUE, 'Desarrollo personal,Te ayudó en el desarrollo del plan de vida', 
 'Capacidad del trabajo grupal,Habilidad comunicativa', 
 TRUE, 'Porque la formación está relacionada con la práctica laboral,Por el desarrollo de los conocimientos básicos para el desempeño laboral', 
 'Recursos Tecnológicos,Infraestructura', 
 TRUE, 'La metodología de la Alternancia Educativa,El perfil ocupacional es actualizado y da mayores posibilidades de empleo', 
 FALSE, TRUE, 'Actualizar la infraestructura y recursos tecnológicos'),

(8, TRUE, 'Un sueldo adecuado en función a tu experiencia personal,Desarrollo personal', 
 'Dominio de su especialidad,Capacidad del trabajo grupal', 
 TRUE, 'Por el equipamiento especializado de la carrera,Porque la formación está relacionada con la práctica laboral', 
 'Actualización de los Docente,Recursos Tecnológicos', 
 TRUE, 'El equipamiento con que cuenta la carrera permite una buena formación tecnológica,La metodología de la Alternancia Educativa', 
 TRUE, TRUE, 'Mejorar los recursos tecnológicos y actualizar a los docentes'),

(9, TRUE, 'Un sueldo adecuado en función a tu experiencia personal,Desarrollo personal', 
 'Dominio de su especialidad,Capacidad creativa innovación', 
 TRUE, 'Por el equipamiento especializado de la carrera,Por el desarrollo de los conocimientos básicos para el desempeño laboral', 
 'Recursos Tecnológicos,Laboratorios', 
 TRUE, 'El equipamiento con que cuenta la carrera permite una buena formación tecnológica,Los docentes de la carrera tienen experiencia y están actualizados en la especialidad', 
 TRUE, TRUE, 'Mejorar los laboratorios y recursos tecnológicos'),

(10, TRUE, 'Desarrollo personal,Te ayudó en el desarrollo del plan de vida', 
 'Organización del trabajo,Capacidad del trabajo grupal', 
 TRUE, 'Por el desarrollo de los conocimientos básicos para el desempeño laboral,Porque la formación está relacionada con la práctica laboral', 
 'Actualización de los Docente,Metodología de enseñanza del Docente', 
 TRUE, 'La metodología de la Alternancia Educativa,La formación y adquisición de habilidades básicas mejoran el desempeño laboral', 
 FALSE, TRUE, 'Mejorar la metodología de enseñanza y actualizar a los docentes');

-- =====================================================
-- PASO 9: VERIFICACIÓN FINAL
-- =====================================================

-- Verificar datos insertados
SELECT 'ESTADOS_CIVIL' as tabla, COUNT(*) as registros FROM estado_civil
UNION ALL
SELECT 'CARRERAS_PROFESIONALES', COUNT(*) FROM carrera_profesional
UNION ALL
SELECT 'ACTIVIDADES_ECONOMICAS', COUNT(*) FROM actividad_economica
UNION ALL
SELECT 'EMPRESAS', COUNT(*) FROM empresa
UNION ALL
SELECT 'EGRESADOS', COUNT(*) FROM EGRESADO
UNION ALL
SELECT 'DETALLES_EGRESADOS', COUNT(*) FROM detalle_egresado
UNION ALL
SELECT 'CERTIFICACIONES', COUNT(*) FROM certificacion
UNION ALL
SELECT 'ENCUESTAS_EGRESADOS', COUNT(*) FROM encuesta_egresado
UNION ALL
SELECT 'EVALUACIONES_FORMACION', COUNT(*) FROM evaluacion_formacion;

