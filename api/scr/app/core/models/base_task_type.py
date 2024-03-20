from typing import TYPE_CHECKING, Dict

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB


from .base import Base

if TYPE_CHECKING:
    from .task_type import TaskType


class BaseTaskType(Base):
    __tablename__ = "base_task_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    settings: Mapped[Dict[str, str]] = mapped_column(JSONB, nullable=True)

    task_types: Mapped[list["TaskType"]] = relationship(back_populates="base_type")
