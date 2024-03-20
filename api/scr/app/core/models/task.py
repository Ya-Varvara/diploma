from typing import Any, Dict, TYPE_CHECKING
from datetime import datetime

from sqlalchemy import (
    String,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .task_type import TaskType
    from .test_task import TestTask
    from .user import User


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("task_types.id"))
    description_data: Mapped[str] = mapped_column(String(2048))
    condition_data: Mapped[Dict[str, Any]] = mapped_column(JSONB)
    answer_data: Mapped[Dict[str, Any]] = mapped_column(JSONB)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted: Mapped[bool]

    type_name: Mapped["TaskType"] = relationship(back_populates="tasks")
    task_variants: Mapped[list["TestTask"]] = relationship(back_populates="task")
    user: Mapped["User"] = relationship(back_populates="tasks")
