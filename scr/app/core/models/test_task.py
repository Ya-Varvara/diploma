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
    from .test import Test
    from .task import Task


class TestTask(Base):
    __tablename__ = "test_task"

    variant: Mapped[int]
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    is_given: Mapped[bool]

    test: Mapped["Test"] = relationship(back_populates="test_variants")
    task: Mapped["Task"] = relationship(back_populates="task_variants")
