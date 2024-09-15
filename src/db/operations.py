from fastapi import Depends, HTTPException
from src.db.models import Tasks
from src.db.db import get_db
from sqlalchemy.orm import Session
from src.api.models import TaskCreate, ImageCreate, DeleteTask
from src.db.models import Images
from sqlalchemy.future import select

async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Tasks(
        name=task.name,
        )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def create_images(task: ImageCreate, path_task: str, db: Session = Depends(get_db)):
    db_images = Images(
        name=task.name,
        path=path_task,
        task_id=task.task_id
        )
    db.add(db_images)
    await db.commit()
    await db.refresh(db_images)
    return db_images

async def delete_task(task: DeleteTask, db: Session = Depends(get_db)):
    result = await db.execute(select(Tasks).where(Tasks.id == task.task_id))
    task_to_delete = result.scalars().first()
    if task_to_delete is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task_to_delete)
    await db.commit()
