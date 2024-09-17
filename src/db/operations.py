from fastapi import Depends, HTTPException
from src.db.definitions import Gender
from src.db.models import Faces, Images, Tasks
from src.db.db import get_db
from sqlalchemy.orm import Session
from src.api.models import GetTask, TaskCreate, ImageCreate, DeleteTask
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Tasks(
        name=task.name,
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def create_images(
    task: ImageCreate, path_task: str, db: Session = Depends(get_db)
):
    db_images = Images(name=task.name, path=path_task, task_id=task.task_id)
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


async def create_face(
    image_id, bounding_box, gender, age, db: Session = Depends(get_db)
):
    db_face = Faces(
        image_id=image_id, bounding_dox=bounding_box, gender=gender, age=age
    )
    db.add(db_face)
    await db.commit()
    await db.refresh(db_face)
    return db_face


async def get_task_details(task_id: GetTask, db: Session = Depends(get_db)):
    stmt = select(Tasks).options(selectinload(Tasks.images)).where(Tasks.id == task_id)
    result = await db.execute(stmt)
    task = result.scalars().first()

    if not task:
        return {"error": "Task not found"}

    total_faces = 0
    male_count = 0
    female_count = 0
    total_age_male = 0
    total_age_female = 0

    images_data = []

    for image in task.images:
        image_info = {"name": image.name, "faces": []}

        for face in image.faces:
            face_info = {
                "bounding_box": face.bounding_dox,
                "gender": face.gender,
                "age": face.age,
            }
            image_info["faces"].append(face_info)
            total_faces += 1
            if face.gender == Gender.male:
                male_count += 1
                total_age_male += face.age
            elif face.gender == Gender.female:
                female_count += 1
                total_age_female += face.age

        images_data.append(image_info)

    average_age_male = round(total_age_male / male_count if male_count > 0 else 0)
    average_age_female = round(
        total_age_female / female_count if female_count > 0 else 0
    )

    return {
        "task_id": task.id,
        "images": images_data,
        "total_faces": total_faces,
        "male_count": male_count,
        "female_count": female_count,
        "average_age_male": average_age_male,
        "average_age_female": average_age_female,
    }
