from typing import List, Any, Dict, TYPE_CHECKING

from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Column, Integer, Text, String, Boolean, MetaData, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base: DeclarativeMeta = declarative_base()

if TYPE_CHECKING:
    class Task(Base):
        pass


class TaskType(Base):
    __tablename__ = "task_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    data_types: Mapped[List[str]] = mapped_column(ARRAY(String))
    answer_type: Mapped[List[str]] = mapped_column(ARRAY(String))

    tasks: Mapped[List[Task]] = relationship(back_populates="type")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    type: Mapped[TaskType] = relationship(back_populates="id")
    data: Mapped[Dict[str, Any]] = mapped_column(JSONB)


