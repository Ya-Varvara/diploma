from typing import TYPE_CHECKING, Dict, List, Any

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSON


from .base import Base

if TYPE_CHECKING:
    from .task_type import TaskType


class BaseTaskType(Base):
    __tablename__ = "base_task_types"

    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    settings: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)

    task_types: Mapped[List["TaskType"]] = relationship(back_populates="base_type")
