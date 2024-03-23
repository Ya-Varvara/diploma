from typing import TYPE_CHECKING, Any, Dict, List
from datetime import datetime

from sqlalchemy import String, ARRAY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP

from .base import Base

if TYPE_CHECKING:
    from .task import Task
    from .user import User
    from .base_task_type import BaseTaskType
    from .form import Form
    from .test import TestTaskType


class TaskType(Base):
    __tablename__ = "task_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    base_task_type: Mapped[int] = mapped_column(
        ForeignKey("base_task_types.id"), nullable=True
    )
    settings: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted: Mapped[bool]

    tasks: Mapped[list["Task"]] = relationship(back_populates="type_name")
    user: Mapped["User"] = relationship(back_populates="task_types")
    base_type: Mapped["BaseTaskType"] = relationship(back_populates="task_types")
    tests: Mapped[List["TestTaskType"]] = relationship(back_populates="task_type")

    condition_forms: Mapped[List["Form"]] = relationship(
        secondary="task_types_condition_forms", back_populates="condition_task_type_ids"
    )
    answer_forms: Mapped[List["Form"]] = relationship(
        secondary="task_types_answer_forms", back_populates="answer_task_type_ids"
    )
