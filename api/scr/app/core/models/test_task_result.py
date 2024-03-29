from typing import Any, Dict, TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import JSONB, BYTEA
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .test_task import TestTask


class TestTaskResult(Base):
    __tablename__ = "test_task_result"

    test_task_id: Mapped[int] = mapped_column(ForeignKey("test_task.id"))
    answer: Mapped[Dict[str, Any]] = mapped_column(JSONB)
    data: Mapped[bytes] = mapped_column(BYTEA, nullable=True)
    student_info: Mapped[Dict[str, Any]] = mapped_column(JSONB)

    test: Mapped["TestTask"] = relationship(back_populates="result")
