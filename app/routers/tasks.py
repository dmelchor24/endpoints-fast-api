from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, MessageResponse
from app.crud import task as crud

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, summary="1. Crear tarea")
async def create(data: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_task(db, data)

@router.get("/", response_model=list[TaskResponse], summary="2. Listar tareas")
async def list_tasks(db: AsyncSession = Depends(get_db)):
    return await crud.get_tasks(db)

@router.get("/{task_id}", response_model=TaskResponse, summary="3. Obtener tarea por ID")
async def get(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await crud.get_task(db, task_id)
    if not task:
        raise HTTPException(404, "Tarea no encontrada")
    return task

@router.put("/{task_id}", response_model=TaskResponse, summary="4. Actualizar tarea por ID")
async def update(task_id: int, data: TaskUpdate, db: AsyncSession = Depends(get_db)):
    task = await crud.update_task(db, task_id, data)
    if not task:
        raise HTTPException(404, "Tarea no encontrada")
    return task

@router.delete("/{task_id}", response_model=MessageResponse, summary="5. Eliminar tarea por ID")
async def delete(task_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(404, "Tarea no encontrada")
    return {"message": "Eliminada correctamente"}