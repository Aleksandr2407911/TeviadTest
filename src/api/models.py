from pydantic import BaseModel

class TaskCreate(BaseModel):
    name: str
    all_faces: int = 0
    male_female_faces: int = 0
    average_age_male: int = 0
    average_age_female: int = 0