from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, MessageResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Convierte una fila de SQLite en un diccionario
def row_to_dict(row):
    return dict(row)

# CREATE - Crear nueva tarea
@router.post(
    "", 
    response_model=TaskResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="1. Crear nueva tarea"
)

# Crea una nueva tarea en la base de datos
def create_task(task: TaskCreate):
    now = datetime.now().isoformat()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO tasks (title, description, created_at, updated_at) 
               VALUES (?, ?, ?, ?)""",
            (task.title, task.description, now, now)
        )
        conn.commit()
        task_id = cursor.lastrowid

    return {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "created_at": now,
        "updated_at": now
    }

# READ - Leer tareas
@router.get(
    "", 
    response_model=list[TaskResponse],
    summary="2. Listar todas las tareas"
)

# Lista todas las tareas almacenadas en la base de datos
def list_tasks():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        rows = cursor.fetchall()

    return [row_to_dict(r) for r in rows]

# READ - Leer tareas por ID
@router.get(
    "/{task_id}", 
    response_model=TaskResponse,
    summary="3. Obtener una tarea por ID"
)

# Obtiene una tarea específica por su ID
def get_task(task_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    return row_to_dict(row)

# UPDATE - Actualizar tarea
@router.put(
    "/{task_id}", 
    response_model=TaskResponse,
    summary="4. Actualizar una tarea"
)

# Actualiza una tarea existente
def update_task(task_id: int, task: TaskUpdate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )

        # Combina datos existentes con los nuevos
        data = dict(row)
        data.update(task.dict(exclude_unset=True))
        data["updated_at"] = datetime.now().isoformat()

        cursor.execute(
            """UPDATE tasks 
               SET title = ?, description = ?, updated_at = ? 
               WHERE id = ?""",
            (data["title"], data["description"], data["updated_at"], task_id)
        )
        conn.commit()

    return data

# DELETE - Eliminar tarea
@router.delete(
    "/{task_id}", 
    response_model=MessageResponse, 
    status_code=status.HTTP_200_OK,
    summary="5. Eliminar una tarea"
)

# Elimina una tarea de la base de datos
def delete_task(task_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )
        
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    
    return {"message": "Task deleted successfully"}