-- Script para arreglar permisos de la base de datos Spring
-- Ejecutar como usuario postgres: psql -U postgres -d agenda_spring_db -f fix_permissions.sql

-- Otorgar todos los privilegios al usuario agenda_user
GRANT ALL PRIVILEGES ON DATABASE agenda_spring_db TO agenda_user;

-- Otorgar privilegios en el esquema public
GRANT ALL ON SCHEMA public TO agenda_user;

-- Otorgar privilegios en todas las tablas existentes
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO agenda_user;

-- Otorgar privilegios en todas las secuencias (para SERIAL/IDENTITY)
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO agenda_user;

-- Otorgar privilegios en todas las funciones
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO agenda_user;

-- Hacer que los privilegios sean permanentes para tablas futuras
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO agenda_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO agenda_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO agenda_user;

-- Verificar permisos
\dt
SELECT 'Permisos otorgados correctamente' AS mensaje;
