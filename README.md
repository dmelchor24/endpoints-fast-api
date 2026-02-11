# Task API - FastAPI

API RESTful para la gestión de tareas, desarrollada con FastAPI y SQLite.

## Características

- ✅ API RESTful completa con operaciones CRUD
- ✅ Documentación automática con Swagger UI y ReDoc
- ✅ Validación de datos con Pydantic
- ✅ Base de datos SQLite (sin configuración adicional)
- ✅ Código completamente documentado y comentado
- ✅ Arquitectura modular y escalable
- ✅ Health check endpoint para monitoreo

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para construir APIs
- **Pydantic**: Validación de datos y serialización
- **SQLite**: Base de datos ligera y sin servidor
- **Uvicorn**: Servidor ASGI de alto rendimiento

## Estructura del Proyecto

```
endpoints-fast-api/
├── app/
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── core/
│   │   └── database.py      # Configuración y utilidades de BD
│   ├── routers/
│   │   ├── health.py        # Endpoints de health check
│   │   └── tasks.py         # Endpoints CRUD de tareas
│   └── schemas/
│       └── task.py          # Modelos Pydantic para validación
├── requirements.txt         # Dependencias del proyecto
├── tasks.db                 # Base de datos SQLite (se crea automáticamente)
└── README.md                # Documentación del proyecto
└── .gitignore               # Excluye archivos, directorios, etc
```

## Descripción de Módulos

### `app/main.py`
Punto de entrada de la aplicación. Configura FastAPI, registra los routers y gestiona el ciclo de vida de la aplicación (inicialización de la base de datos).

### `app/core/database.py`
Maneja la conexión a SQLite mediante un context manager que garantiza el cierre correcto de conexiones. Incluye la función de inicialización de la base de datos.

### `app/routers/health.py`
Proporciona un endpoint de health check para verificar que la API está funcionando correctamente. Útil para monitoreo y contenedores.

### `app/routers/tasks.py`
Implementa todos los endpoints CRUD para tareas:
- Crear tareas
- Listar todas las tareas
- Obtener una tarea específica
- Actualizar tareas (parcial o completa)
- Eliminar tareas

### `app/schemas/task.py`
Define los esquemas Pydantic para validación de datos:
- `TaskCreate`: Validación al crear tareas
- `TaskUpdate`: Validación al actualizar tareas
- `TaskResponse`: Formato de respuesta de tareas
- `MessageResponse`: Respuestas de confirmación

## API Endpoints

### Root
- `GET /` - Información de bienvenida y enlaces útiles

### Health Check
- `GET /api/v1/health` - Verifica el estado de la API

### Tasks (Tareas)
- `POST /api/v1/tasks` - Crear una nueva tarea
- `GET /api/v1/tasks` - Listar todas las tareas
- `GET /api/v1/tasks/{id}` - Obtener una tarea específica
- `PUT /api/v1/tasks/{id}` - Actualizar una tarea
- `DELETE /api/v1/tasks/{id}` - Eliminar una tarea

## Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd task-api
   ```

2. **Crear un entorno virtual (recomendado)**
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

4. **Ejecutar el servidor**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Acceder a la aplicación**
   - API: http://localhost:8000
   - Documentación Swagger: http://localhost:8000/docs
   - Documentación ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/api/v1/health

## Características del Código

### Validación de Datos
Todos los endpoints utilizan Pydantic para validar automáticamente:
- Tipos de datos correctos
- Campos obligatorios
- Longitud de strings (título máx. 200 caracteres, descripción máx. 1000)

### Manejo de Errores
La API devuelve códigos HTTP apropiados:
- `200 OK` - Operación exitosa
- `201 Created` - Recurso creado exitosamente
- `404 Not Found` - Recurso no encontrado
- `422 Unprocessable Entity` - Error de validación

### Documentación
- Docstrings en todas las funciones
- Comentarios explicativos en el código
- Ejemplos en los esquemas Pydantic
- Documentación automática generada por FastAPI

### Buenas Prácticas
- Context managers para gestión de recursos
- Separación de responsabilidades (routers, schemas, database)
- Uso de códigos de estado HTTP semánticos
- Validación de entrada y salida de datos
- Mensajes de error descriptivos

---

**Desarrollado con fines educativos para aprender FastAPI y desarrollo de APIs RESTful.**