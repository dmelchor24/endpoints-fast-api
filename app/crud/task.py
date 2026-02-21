from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.models.task import Task

async def create_task(db: AsyncSession, data):
    task = Task(**data.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()

async def get_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()

async def update_task(db: AsyncSession, task_id: int, data):
    task = await get_task(db, task_id)
    if not task:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task_id: int):
    task = await get_task(db, task_id)
    if not task:
        return False

    await db.delete(task)
    await db.commit()
    return True