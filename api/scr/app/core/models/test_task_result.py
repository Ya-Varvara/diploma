from typing import Any, Dict, TYPE_CHECKING, Optional
from datetime import datetime

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .test_task import TestTask


class TestTaskResult(Base):
    __tablename__ = "test_task_result"

    test_task_id: Mapped[int] = mapped_column(ForeignKey("test_task.id"))
    answer: Mapped[Dict[str, Any]] = mapped_column(JSONB)
    student_info: Mapped[Dict[str, Any]] = mapped_column(JSONB)
    start_datetime: Mapped[datetime] = mapped_column(TIMESTAMP)
    end_datetime: Mapped[datetime] = mapped_column(TIMESTAMP)
    is_correct: Mapped[Optional[bool]]

    test: Mapped["TestTask"] = relationship(back_populates="result")
