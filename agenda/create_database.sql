-- Script para crear la base de datos y usuario para Spring Boot
-- Ejecutar este script como usuario postgres

-- Crear usuario (si no existe)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'agenda_user') THEN
        CREATE USER agenda_user WITH PASSWORD 'password123';
    END IF;
END
$$;

-- Crear base de datos usando template0 para evitar problemas de collation
DROP DATABASE IF EXISTS agenda_spring_db;
CREATE DATABASE agenda_spring_db
    WITH
    TEMPLATE = template0
    OWNER = agenda_user
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Mexico.1252'
    LC_CTYPE = 'Spanish_Mexico.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Conectar a la base de datos
\c agenda_spring_db

-- Otorgar privilegios al usuario
GRANT ALL PRIVILEGES ON DATABASE agenda_spring_db TO agenda_user;
GRANT ALL ON SCHEMA public TO agenda_user;

-- Crear tabla personas con timestamps automáticos
CREATE TABLE IF NOT EXISTS personas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    direccion TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Crear índices
CREATE INDEX idx_personas_email ON personas(email);

-- Crear función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Crear trigger para updated_at
CREATE TRIGGER update_personas_updated_at
    BEFORE UPDATE ON personas
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insertar datos de ejemplo (opcional)
INSERT INTO personas (nombre, apellido, email, telefono, direccion) VALUES
('Juan', 'Pérez', 'juan.perez@example.com', '555-0101', 'Calle 123, Ciudad'),
('María', 'García', 'maria.garcia@example.com', '555-0102', 'Avenida 456, Ciudad'),
('Carlos', 'López', 'carlos.lopez@example.com', '555-0103', 'Boulevard 789, Ciudad');

-- Verificar que todo se creó correctamente
SELECT 'Base de datos creada exitosamente' AS mensaje;
SELECT * FROM personas;
