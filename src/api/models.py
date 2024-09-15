from pydantic import BaseModel
import uuid

class TaskCreate(BaseModel):
    name: str

class ImageCreate(BaseModel):
    name: str
    task_id: uuid.UUID
    
class DeleteTask(BaseModel):
    task_id: uuid.UUID
