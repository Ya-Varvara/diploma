from typing import TYPE_CHECKING, List

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base

if TYPE_CHECKING:
    from .task_type import TaskType


class TaskTypesConditionForm(Base):
    __tablename__ = "task_types_condition_forms"

    task_type_condition_form_id: Mapped[int] = mapped_column(
        ForeignKey("task_types.id"), primary_key=True, nullable=False
    )
    form_id: Mapped[int] = mapped_column(
        ForeignKey("forms.id"), primary_key=True, nullable=False
    )


class TaskTypesAnswerForm(Base):
    __tablename__ = "task_types_answer_forms"

    task_type_answer_form_id: Mapped[int] = mapped_column(
        ForeignKey("task_types.id"), primary_key=True, nullable=False
    )
    form_id: Mapped[int] = mapped_column(
        ForeignKey("forms.id"), primary_key=True, nullable=False
    )


class Form(Base):
    __tablename__ = "forms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    short_name: Mapped[str] = mapped_column(String(64), nullable=False)
    condition_form: Mapped[bool]
    answer_form: Mapped[bool]

    answer_task_type_ids: Mapped[List["TaskType"]] = relationship(
        secondary="task_types_answer_forms", back_populates="answer_forms"
    )
    condition_task_type_ids: Mapped[List["TaskType"]] = relationship(
        secondary="task_types_condition_forms", back_populates="condition_forms"
    )
