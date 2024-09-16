import sqlalchemy
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    as_declarative,
    declared_attr,
    mapped_column,
)
from sqlalchemy import(
    JSON,
    CheckConstraint,
    ForeignKey,
    Integer,
    MetaData
)

from sqlalchemy.dialects.postgresql import UUID
import uuid
from stringcase import snakecase
from src.db.definitions import Gender

@as_declarative()
class AbstractModel:
    metadata = MetaData()
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key = True, default = uuid.uuid4
    )

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return snakecase(cls.__name__)

class Tasks(AbstractModel):
    name: Mapped[str] = mapped_column()
    all_faces: Mapped[int] = mapped_column(default=0)
    male_female_faces: Mapped[int] = mapped_column(default=0)
    average_age_male: Mapped[int] = mapped_column(default=0)
    average_age_female: Mapped[int] = mapped_column(default=0)

    images: Mapped[list["Images"]] = relationship("Images", back_populates = "tasks", uselist=True,
                                                  cascade="all, delete-orphan", passive_deletes=True)

class Images(AbstractModel):
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column()
    path: Mapped[str] = mapped_column()

    tasks: Mapped["Tasks"] = relationship("Tasks", back_populates = "images", uselist = False)
    faces: Mapped[list["Faces"]] = relationship("Faces", back_populates = "images", uselist=True,
                                                cascade="all, delete-orphan", passive_deletes=True)

class Faces(AbstractModel):
    image_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("images.id", ondelete="CASCADE"), nullable = False)
    bounding_dox: Mapped[dict] = mapped_column(JSON)
    gender: Mapped[Gender] = mapped_column()
    age: Mapped[int] = mapped_column(CheckConstraint("age >= 1 AND age <= 200"), nullable=False)

    images: Mapped["Images"] = relationship("Images", back_populates = "faces")
