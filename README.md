# Agenda de Contactos - Sistema con Bases de Datos Sincronizadas

Sistema de gestión de agenda de contactos desarrollado con **FastAPI** y **Spring Boot**, implementando sincronización unidireccional entre dos bases de datos PostgreSQL independientes.

## 📋 Descripción

Aplicación full-stack que permite gestionar una agenda de personas con operaciones CRUD completas. El sistema utiliza dos APIs REST independientes que se comunican entre sí para mantener sincronizadas las operaciones de creación de nuevos contactos.

### Características principales:
- **FastAPI** (Python) - API principal en puerto 8888
- **Spring Boot** (Java) - API secundaria en puerto 8080
- **PostgreSQL** - Base de datos independiente para cada API
- **Sincronización unidireccional** - Las creaciones en FastAPI se replican automáticamente a Spring Boot
- Interfaz web HTML con Jinja2 templates
- API REST completa con documentación Swagger/OpenAPI

## 🏗️ Estructura del Proyecto

```
AgendaFastAPISpring/
│
├── FastAPI/                          # Backend en Python con FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # Punto de entrada y rutas principales
│   │   ├── models.py                 # Modelos SQLAlchemy
│   │   ├── schemas.py                # Esquemas Pydantic para validación
│   │   ├── database.py               # Configuración de base de datos
│   │   ├── crud.py                   # Operaciones CRUD
│   │   ├── spring_client.py          # Cliente HTTP para sincronización con Spring
│   │   └── templates/                # Templates HTML Jinja2
│   │       ├── index.html
│   │       ├── formulario.html
│   │       └── detalle.html
│   └── requirements.txt              # Dependencias Python
│
└── agenda/                           # Backend en Java con Spring Boot
    ├── src/
    │   ├── main/
    │   │   ├── java/com/example/agenda/
    │   │   │   ├── AgendaApplication.java      # Aplicación principal
    │   │   │   ├── controllers/
    │   │   │   │   ├── PersonaController.java  # REST Controller
    │   │   │   │   └── WebController.java      # Web Controller (Thymeleaf)
    │   │   │   ├── models/
    │   │   │   │   └── Persona.java            # Entidad JPA
    │   │   │   ├── repositories/
    │   │   │   │   └── PersonaRepository.java  # JPA Repository
    │   │   │   └── services/
    │   │   │       ├── PersonaService.java     # Lógica de negocio
    │   │   │       └── FastAPIClient.java      # Cliente para comunicación
    │   │   └── resources/
    │   │       └── application.properties      # Configuración Spring
    │   └── test/
    ├── pom.xml                        # Dependencias Maven
    ├── create_database.sql            # Script de creación de BD
    └── fix_permissions.sql            # Script de permisos
```

## 🗄️ Diseño de Base de Datos

Ambos sistemas utilizan PostgreSQL con una estructura de tabla idéntica:

### Tabla: `personas`

| Campo       | Tipo                   | Restricciones           | Descripción                    |
|-------------|------------------------|-------------------------|--------------------------------|
| id          | SERIAL (INTEGER)       | PRIMARY KEY             | Identificador único autogenerado|
| nombre      | VARCHAR(100)           | NOT NULL                | Nombre de la persona           |
| apellido    | VARCHAR(100)           | NOT NULL                | Apellido de la persona         |
| email       | VARCHAR(100)           | NOT NULL, UNIQUE        | Correo electrónico único       |
| telefono    | VARCHAR(20)            | NULLABLE                | Número de teléfono             |
| direccion   | TEXT                   | NULLABLE                | Dirección completa             |
| created_at  | TIMESTAMP WITH TIME ZONE| DEFAULT CURRENT_TIMESTAMP| Fecha de creación             |
| updated_at  | TIMESTAMP WITH TIME ZONE| AUTO-UPDATE             | Fecha de última modificación   |

**Índices:**
- `PRIMARY KEY` en `id`
- `UNIQUE INDEX` en `email`
- `INDEX` en `email` para búsquedas rápidas

**Triggers:**
- `update_personas_updated_at`: Actualiza automáticamente `updated_at` en cada UPDATE

### Bases de Datos

1. **FastAPI DB**: `agenda_fastapi_db` (generada automáticamente por SQLAlchemy)
2. **Spring Boot DB**: `agenda_spring_db` (creada mediante `create_database.sql`)
   - Usuario: `agenda_user`
   - Contraseña: `password123`
   - Collation: `Spanish_Mexico.1252`

## 🚀 Cómo Ejecutar

### Prerequisitos

- **Python 3.8+**
- **Java 17+**
- **Maven 3.6+**
- **PostgreSQL 12+**

### 1. Configurar Base de Datos

```bash
# Conectarse a PostgreSQL como superusuario
psql -U postgres

# Ejecutar el script de creación para Spring Boot
\i agenda/create_database.sql

# La base de datos para FastAPI se crea automáticamente
```

### 2. Ejecutar FastAPI

```bash
# Navegar al directorio FastAPI
cd FastAPI

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload
```

**Accesos:**
- API REST: http://localhost:8888
- Documentación Swagger: http://localhost:8888/docs
- Interfaz Web: http://localhost:8888/web/

### 3. Ejecutar Spring Boot

```bash
# Navegar al directorio agenda
cd agenda

# Compilar y ejecutar con Maven
mvn spring-boot:run

# O ejecutar el JAR después de compilar
mvn clean package
java -jar target/agenda-0.0.1-SNAPSHOT.jar
```

**Accesos:**
- API REST: http://localhost:8080
- Interfaz Web: http://localhost:8080

## 🔄 Sincronización de Datos

El sistema implementa **sincronización unidireccional**:

- ✅ **CREATE**: Cuando se crea una persona en FastAPI, automáticamente se replica a Spring Boot
- ❌ **UPDATE/DELETE**: No se sincronizan debido a que los IDs autogenerados difieren entre bases de datos

### Flujo de Sincronización

1. Usuario crea contacto en FastAPI → Se guarda en BD de FastAPI
2. FastAPI envía petición HTTP POST a Spring Boot
3. Spring Boot guarda el contacto en su propia BD
4. Ambas BDs tienen el registro (con diferentes IDs)

## 🛠️ Tecnologías Utilizadas

### FastAPI (Python)
- **FastAPI** 0.104.1 - Framework web moderno
- **SQLAlchemy** 2.0.23 - ORM
- **Psycopg2** 2.9.9 - Driver PostgreSQL
- **Pydantic** 2.5.0 - Validación de datos
- **Jinja2** 3.1.2 - Motor de templates
- **Uvicorn** 0.24.0 - Servidor ASGI
- **httpx** 0.25.2 - Cliente HTTP asíncrono

### Spring Boot (Java)
- **Spring Boot** 3.x - Framework principal
- **Spring Data JPA** - Persistencia de datos
- **PostgreSQL Driver** - Conexión a BD
- **Hibernate** - ORM
- **Thymeleaf** - Motor de templates (opcional)
- **Maven** - Gestión de dependencias

## 📡 Endpoints Principales

### FastAPI
- `GET /` - Mensaje de bienvenida
- `GET /personas/` - Listar todas las personas
- `GET /personas/{id}` - Obtener persona por ID
- `POST /personas/` - Crear nueva persona (sincroniza con Spring)
- `PUT /personas/{id}` - Actualizar persona
- `DELETE /personas/{id}` - Eliminar persona
- `GET /web/` - Interfaz web

### Spring Boot
- `GET /api/personas` - Listar todas las personas
- `GET /api/personas/{id}` - Obtener persona por ID
- `POST /api/personas` - Crear nueva persona
- `PUT /api/personas/{id}` - Actualizar persona
- `DELETE /api/personas/{id}` - Eliminar persona
- `GET /` - Interfaz web

## 📝 Notas Adicionales

- Las contraseñas y credenciales en este proyecto son solo para desarrollo
- Para producción, usar variables de entorno y secrets managers
- Los puertos 8080 y 8888 deben estar disponibles
- La sincronización requiere que ambos servicios estén ejecutándose simultáneamente
