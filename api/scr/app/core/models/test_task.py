from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .test import Test
    from .task import Task
    from .test_task_result import TestTaskResult
    from .uploaded_file import UploadedFile


class TestTask(Base):
    __tablename__ = "test_task"

    variant: Mapped[int]
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    is_given: Mapped[bool]

    test: Mapped["Test"] = relationship(back_populates="test_variants")
    task: Mapped["Task"] = relationship(back_populates="task_variants")
    result: Mapped["TestTaskResult"] = relationship(back_populates="test")
    uploaded_file: Mapped["UploadedFile"] = relationship(back_populates="test_task")
