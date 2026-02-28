# Task API - FastAPI Async

API RESTful asíncrona para la gestión de tareas, desarrollada con FastAPI, PostgreSQL y SQLAlchemy.

## Características

- ✅ API RESTful completa con operaciones CRUD asíncronas
- ✅ Documentación automática con Swagger UI y ReDoc
- ✅ Validación de datos con Pydantic v2
- ✅ Base de datos PostgreSQL con SQLAlchemy async
- ✅ Arquitectura modular y escalable
- ✅ Health check endpoint para monitoreo
- ✅ Dockerizado con Docker Compose
- ✅ Gestión de variables de entorno con python-dotenv
- ✅ Migraciones con Alembic

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para construir APIs
- **SQLAlchemy 2.0**: ORM asíncrono para Python
- **PostgreSQL**: Base de datos relacional robusta
- **asyncpg**: Driver asíncrono de PostgreSQL
- **Pydantic**: Validación de datos y serialización
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Docker & Docker Compose**: Contenedorización y orquestación
- **Alembic**: Herramienta de migraciones de base de datos

## Estructura del Proyecto

```
task-api/
├── app/
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── core/
│   │   └── database.py      # Configuración de SQLAlchemy async y PostgreSQL
│   ├── models/
│   │   └── task.py          # Modelos SQLAlchemy (ORM)
│   ├── schemas/
│   │   └── task.py          # Esquemas Pydantic para validación
│   ├── crud/
│   │   └── task.py          # Operaciones CRUD asíncronas
│   └── routers/
│       ├── health.py        # Endpoints de health check
│       └── tasks.py         # Endpoints CRUD de tareas
├── .env                     # Variables de entorno
├── .dockerignore            # Archivos excluidos de Docker
├── .gitignore               # Archivos excluidos de Git
├── docker-compose.yaml      # Orquestación de contenedores
├── Dockerfile               # Imagen Docker de la aplicación
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Documentación del proyecto
```

## Descripción de Módulos

### `app/main.py`
Punto de entrada de la aplicación. Configura FastAPI con un lifespan asíncrono que crea las tablas de la base de datos al iniciar. Registra los routers de tasks y health.

### `app/core/database.py`
Configura SQLAlchemy 2.0 con soporte asíncrono usando asyncpg. Define el engine asíncrono, la sesión y el Base declarativo. Incluye una dependencia `get_db()` para inyección en los endpoints.

### `app/models/task.py`
Define el modelo ORM `Task` con SQLAlchemy:
- `id`: Clave primaria autoincremental
- `title`: Título de la tarea (máx. 255 caracteres)
- `description`: Descripción opcional (texto largo)
- `created_at`: Timestamp de creación
- `updated_at`: Timestamp de última actualización

### `app/schemas/task.py`
Define los esquemas Pydantic para validación y serialización:
- `TaskCreate`: Validación al crear tareas
- `TaskUpdate`: Validación al actualizar tareas (campos opcionales)
- `TaskResponse`: Formato de respuesta de tareas
- `TaskListResponse`: Respuesta para listado de tareas
- `MessageResponse`: Respuestas de confirmación

### `app/crud/task.py`
Implementa las operaciones CRUD asíncronas:
- `create_task()`: Crea una nueva tarea
- `get_task()`: Obtiene una tarea por ID
- `get_tasks()`: Lista todas las tareas
- `update_task()`: Actualiza una tarea existente
- `delete_task()`: Elimina una tarea

### `app/routers/tasks.py`
Define los endpoints de la API para tareas con operaciones CRUD completas.

### `app/routers/health.py`
Proporciona un endpoint de health check para verificar que la API está funcionando correctamente.

## API Endpoints

### Root
- `GET /` - Información de bienvenida

### Health Check
- `GET /api/v1/health` - Verifica el estado de la API y devuelve timestamp

### Tasks (Tareas)
- `POST /api/v1/tasks` - Crear una nueva tarea
- `GET /api/v1/tasks` - Listar todas las tareas
- `GET /api/v1/tasks/{id}` - Obtener una tarea específica por ID
- `PUT /api/v1/tasks/{id}` - Actualizar una tarea existente
- `DELETE /api/v1/tasks/{id}` - Eliminar una tarea

## Instalación y Ejecución

### Requisitos Previos
- Docker y Docker Compose instalados
- Git (para clonar el repositorio)

### Opción 1: Ejecución con Docker (Recomendado)

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd task-api
   ```

2. **Configurar variables de entorno**
   
   El archivo `.env` ya está configurado con:
   ```
   DATABASE_URL=postgresql+asyncpg://fastapi_user_pg:fastapi_pass_pg@postgres:5432/tasks_db
   ```

3. **Levantar los servicios con Docker Compose**
   ```bash
   docker compose up -d
   ```
   
   Esto iniciará:
   - PostgreSQL en el puerto 6000 (mapeado desde 5432)
   - FastAPI en el puerto 8000

4. **Verificar que los contenedores están corriendo**
   ```bash
   docker compose ps
   ```

5. **Acceder a la aplicación**
   - API: http://localhost:8000
   - Documentación Swagger: http://localhost:8000/docs
   - Documentación ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/api/v1/health

6. **Ver logs de la aplicación**
   ```bash
   docker compose logs -f api
   ```

7. **Detener los servicios**
   ```bash
   docker compose down
   ```

8. **Detener y eliminar volúmenes (limpieza completa)**
   ```bash
   docker compose down -v
   ```

### Opción 2: Ejecución Local (Sin Docker)

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd task-api
   ```

2. **Crear un entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar PostgreSQL local**
   
   Asegúrate de tener PostgreSQL instalado y crea una base de datos. Luego actualiza el archivo `.env`:
   ```
   DATABASE_URL=postgresql+asyncpg://tu_usuario:tu_password@localhost:5432/tasks_db
   ```

5. **Ejecutar la aplicación**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Acceder a la aplicación**
   - API: http://localhost:8000
   - Documentación: http://localhost:8000/docs

### Comandos Útiles de Docker

**Conectarse a la base de datos PostgreSQL:**
```bash
docker exec -it fastapi_postgres psql -U fastapi_user_pg -d tasks_db
```

**Reconstruir las imágenes:**
```bash
docker compose build --no-cache
```

**Ver logs de PostgreSQL:**
```bash
docker compose logs -f postgres
```

## Características del Código

### Arquitectura Asíncrona
- Uso de `async/await` en todas las operaciones de base de datos
- SQLAlchemy 2.0 con soporte asíncrono completo
- Driver asyncpg para PostgreSQL de alto rendimiento
- Sesiones asíncronas con context managers

### Validación de Datos
Todos los endpoints utilizan Pydantic v2 para validar automáticamente:
- Tipos de datos correctos
- Campos obligatorios y opcionales
- Longitud de strings (título máx. 200 caracteres, descripción máx. 1000)
- Ejemplos en los esquemas para documentación

### Manejo de Errores
La API devuelve códigos HTTP apropiados:
- `200 OK` - Operación exitosa
- `201 Created` - Recurso creado exitosamente (implícito en POST)
- `404 Not Found` - Recurso no encontrado
- `422 Unprocessable Entity` - Error de validación

### Separación de Responsabilidades
- **Models**: Definición de tablas con SQLAlchemy ORM
- **Schemas**: Validación y serialización con Pydantic
- **CRUD**: Lógica de acceso a datos
- **Routers**: Definición de endpoints y manejo de requests
- **Core**: Configuración de base de datos y dependencias

### Buenas Prácticas
- Uso de dependency injection con `Depends()`
- Context managers para gestión de sesiones de BD
- Variables de entorno para configuración sensible
- Dockerización para portabilidad
- Timestamps automáticos en modelos
- Validación de entrada y salida de datos
- Documentación automática con OpenAPI

### Configuración de Base de Datos
- Soporte para PostgreSQL en Render (conversión automática de URL)
- Pool de conexiones gestionado por SQLAlchemy
- Creación automática de tablas al iniciar la aplicación
- Echo mode activado para debugging de queries SQL

## Ejemplo de Uso

### Crear una tarea
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Aprender FastAPI",
    "description": "Completar el tutorial de FastAPI async"
  }'
```

### Listar todas las tareas
```bash
curl -X GET "http://localhost:8000/api/v1/tasks"
```

### Obtener una tarea específica
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/1"
```

### Actualizar una tarea
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Aprender FastAPI Async",
    "description": "Completar el tutorial avanzado"
  }'
```

### Eliminar una tarea
```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/1"
```

## Dependencias del Proyecto

```
fastapi          # Framework web
uvicorn          # Servidor ASGI
pydantic         # Validación de datos
sqlalchemy       # ORM asíncrono
asyncpg          # Driver PostgreSQL async
alembic          # Migraciones de BD
python-dotenv    # Variables de entorno
```

---

**Desarrollado con fines educativos para aprender FastAPI, SQLAlchemy async y desarrollo de APIs RESTful modernas.**