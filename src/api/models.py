from pydantic import BaseModel
import uuid

# class BoundingBox(BaseModel):
#     x: int
#     y: int
#     width: int
#     height: int

class TaskCreate(BaseModel):
    name: str

class ImageCreate(BaseModel):
    name: str
    task_id: uuid.UUID

class DeleteTask(BaseModel):
    task_id: uuid.UUID

# class FaceCreate(BaseModel):
#     image_id: uuid.UUID
#     bounding_box: BoundingBox
#     gender: str
#     age: str
