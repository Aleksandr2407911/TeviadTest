from typing import Annotated
from fastapi import APIRouter, Depends
from src.db.db import get_db
from sqlalchemy.orm import Session
from src.api.models import TaskCreate
from src.db.operations import create_task

router = APIRouter(prefix="/tevian_test")

@router.post("/create_new_task")
async def create_new_task(task: Annotated[TaskCreate, Depends()], db: Session=Depends(get_db)):
    return await create_task(task, db)