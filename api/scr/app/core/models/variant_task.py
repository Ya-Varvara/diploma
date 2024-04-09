from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .task import Task
    from .variants_task_result import VariantsTaskResult


class VariantTask(Base):
    __tablename__ = "variants_tasks"

    variant_id: Mapped[int] = mapped_column(ForeignKey("variants.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))

    task: Mapped["Task"] = relationship(back_populates="task_variants")
    task_result: Mapped["VariantsTaskResult"] = relationship(back_populates="variant_task")
