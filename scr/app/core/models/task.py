from typing import List, Any, Dict, TYPE_CHECKING

from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    Boolean,
    MetaData,
    ARRAY,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .task_type import TaskType
    from .test_task import TestTask


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("task_types.id"))
    data: Mapped[Dict[str, Any]] = mapped_column(JSONB)

    type_name: Mapped["TaskType"] = relationship(back_populates="tasks")
    task_variants: Mapped[list["TestTask"]] = relationship(back_populates="task")
