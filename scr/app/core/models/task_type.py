from typing import List, Any, Dict, TYPE_CHECKING

from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Column, Integer, Text, String, Boolean, MetaData, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .task import Task


class TaskType(Base):
    __tablename__ = "task_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    data_types: Mapped[List[str]] = mapped_column(ARRAY(String))
    answer_type: Mapped[List[str]] = mapped_column(ARRAY(String))

    tasks: Mapped[list["Task"]] = relationship(back_populates="type_name")
