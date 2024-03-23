from typing import Any, Dict, TYPE_CHECKING, List
from datetime import datetime, time

from sqlalchemy import (
    String,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, TIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .test_task import TestTask
    from .task_type import TaskType


class TestTaskType(Base):
    __tablename__ = "test_task_types"

    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"))
    task_type_id: Mapped[int] = mapped_column(ForeignKey("task_types.id"))
    number: Mapped[int]

    test: Mapped["Test"] = relationship(back_populates="task_types")
    task_type: Mapped["TaskType"] = relationship(back_populates="tests")


class Test(Base):
    __tablename__ = "tests"

    name: Mapped[str] = mapped_column(String(64))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    start_datetime: Mapped[datetime] = mapped_column(TIMESTAMP)
    end_datetime: Mapped[datetime] = mapped_column(TIMESTAMP)
    test_time: Mapped[time] = mapped_column(TIME)
    variants_number: Mapped[int]
    link: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted: Mapped[bool]

    user: Mapped["User"] = relationship(back_populates="tests")
    test_variants: Mapped[list["TestTask"]] = relationship(back_populates="test")
    task_types: Mapped[List["TestTaskType"]] = relationship(back_populates="test")
