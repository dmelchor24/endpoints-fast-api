from fastapi import FastAPI
from app.routers import tasks, health
from app.core.database import init_db
from contextlib import asynccontextmanager

# Gestiona el ciclo de vida de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Inicializar la base de datos
    init_db()
    yield
    # Shutdown: Aquí se pueden agregar tareas de limpieza si es necesario

# Metadatos de los tags para ordenar y documentar en Swagger
tags_metadata = [
    {
        "name": "Root",
        "description": "Endpoint raíz de la API con información general"
    },
    {
        "name": "Health",
        "description": "Endpoints de verificación de estado y monitoreo"
    },
    {
        "name": "Tasks",
        "description": "Operaciones CRUD para gestión de tareas"
    }
]

# Instancia principal de la aplicación FastAPI
app = FastAPI(
    title="Task API",
    description="API RESTful para gestión de tareas con FastAPI y SQLite",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=tags_metadata
)

# Personaliza el esquema OpenAPI para ordenar los endpoints
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags
    )
    
    # Orden deseado de los endpoints de Tasks
    desired_order = [
        ("post", "/api/v1/tasks"),      # 1. Crear
        ("get", "/api/v1/tasks"),       # 2. Listar
        ("get", "/api/v1/tasks/{task_id}"),  # 3. Obtener
        ("put", "/api/v1/tasks/{task_id}"),  # 4. Actualizar
        ("delete", "/api/v1/tasks/{task_id}") # 5. Eliminar
    ]
    
    # Reordenar los paths según el orden deseado
    if "paths" in openapi_schema:
        new_paths = {}
        
        # Primero agregar los endpoints en el orden deseado
        for method, path in desired_order:
            if path in openapi_schema["paths"]:
                if path not in new_paths:
                    new_paths[path] = {}
                if method in openapi_schema["paths"][path]:
                    new_paths[path][method] = openapi_schema["paths"][path][method]
        
        # Luego agregar cualquier otro endpoint que no esté en la lista
        for path, methods in openapi_schema["paths"].items():
            if path not in new_paths:
                new_paths[path] = methods
            else:
                for method, details in methods.items():
                    if method not in new_paths[path]:
                        new_paths[path][method] = details
        
        openapi_schema["paths"] = new_paths
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Asignar la función personalizada
app.openapi = custom_openapi

# Registra los routers de la aplicación
app.include_router(health.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")

# Endpoint raíz de la API
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Task API running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/health"
    }