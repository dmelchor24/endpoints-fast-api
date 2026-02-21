from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "String",
                "description": "String",
                "created_at": "2026-02-09T10:30:00",
                "updated_at": "2026-02-09T10:30:00"
            }
        }

# Esquema para crear una nueva tarea
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción detallada")
    
    class Config:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "title": "String",
                "description": "String"
            }
        }

# Esquema para actualizar una tarea existente
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción detallada")
    
    class Config:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "title": "String",
                "description": "String"
            }
        }

# Esquema de respuesta para una tarea
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "String",
                "description": "String",
                "created_at": "2026-02-09T10:30:00",
                "updated_at": "2026-02-09T10:30:00"
            }
        }

# Esquema de respuesta para listar múltiples tareas
class TaskListResponse(BaseModel):
    total: int
    tasks: List[TaskResponse]

# Esquema de respuesta para mensajes simples
class MessageResponse(BaseModel):
    message: str