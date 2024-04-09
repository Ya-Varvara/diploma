from typing import Any, Dict, TYPE_CHECKING, Optional
from datetime import datetime

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .variant_task import VariantTask


class VariantsTaskResult(Base):
    __tablename__ = "variants_task_result"

    variants_task_id: Mapped[int] = mapped_column(ForeignKey("variants_tasks.id"))
    answer: Mapped[Dict[str, Any]] = mapped_column(JSONB)
    is_correct: Mapped[Optional[bool]]

    variant_task: Mapped["VariantTask"] = relationship(back_populates="task_result")
