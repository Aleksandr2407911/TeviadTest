from fastapi import Depends
from src.db.models import Tasks
from src.db.db import get_db
from sqlalchemy.orm import Session
from src.api.models import TaskCreate

async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Tasks(
        name=task.name,
        all_faces=task.all_faces,
        male_female_faces=task.male_female_faces,
        average_age_male=task.average_age_male,
        average_age_female=task.average_age_female
        )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task