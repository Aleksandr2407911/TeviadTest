import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from src.api.another_func import detect, get_token_tevian
from src.api.auth import verify_credentials
from src.db.db import get_db
from sqlalchemy.orm import Session
from src.api.models import DeleteTask, GetTask, ImageCreate, TaskCreate
from src.db.models import Tasks
from src.db.operations import (
    create_task,
    create_images,
    delete_task,
    create_face,
    get_task_details,
)
from src.db.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/tevian_test", dependencies=[Depends(verify_credentials)])


@router.post("/create_new_task")
async def create_new_task(
    task: Annotated[TaskCreate, Depends()], db: Session = Depends(get_db)
):
    return await create_task(task, db)


@router.post("/load_images")
async def load_images(
    files: list[UploadFile],
    data_image: Annotated[ImageCreate, Depends()],
    db: Session = Depends(get_db),
):
    saved_files = []
    saved_data_images = []
    saved_data_faces = []

    for file in files:
        if not file.filename.endswith(".jpg") and not file.filename.endswith(".jpeg"):
            raise HTTPException(
                status_code=400,
                detail=f"""File format not supported: {file.filename}. Please upload JPEG image only!""",
            )

        file_location = os.path.join(settings.IMAGE_PATH, file.filename)

        try:
            with open(file_location, "wb+") as file_object:
                file_object.write(await file.read())
            saved_files.append(file.filename)
            task = await db.get(Tasks, data_image.task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            image = await create_images(data_image, file_location, db)
            saved_data_images.append(image)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"""An error occured while saving the file
                                {file.filename}: {str(e)}""",
            )
        token = await get_token_tevian(
            settings.TEVIAN_SWAGGER_EMAIL, settings.TEVIAN_SWAGGER_PASSWORD
        )
        detect_data = await detect(token, file_location)
        for data in detect_data["data"]:
            bounding_box = data["bbox"]
            age = data["demographics"]["age"]["mean"]
            gender = data["demographics"]["gender"]
            face = await create_face(image.id, bounding_box, gender, age, db)
            saved_data_faces.append(face)

    return {
        "info ": f"Files saved: {saved_files}\nSaved data images: {saved_data_images}"
    }


@router.delete("/delete_task_use_id")
async def delete_task_use_id(
    task_id: Annotated[DeleteTask, Depends()], db: Session = Depends(get_db)
):
    try:
        await delete_task(task_id, db)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Task not deleted")


@router.get("/get_task")
async def get_task_use_id(
    task: Annotated[GetTask, Depends()], db: AsyncSession = Depends(get_db)
):
    task_id = task.task_id
    try:
        task_details = await get_task_details(task_id, db)
        return task_details
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Task don't get")
