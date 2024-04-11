from typing import Any, Dict, TYPE_CHECKING, Optional
from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .variant import Variant


class VariantResultInfo(Base):
    __tablename__ = "variant_result_info"

    variant_id: Mapped[int] = mapped_column(ForeignKey("test_task.id"))
    students_name: Mapped[str] = mapped_column(String(256))
    students_surname: Mapped[str] = mapped_column(String(256))
    start_datetime: Mapped[datetime] = mapped_column(TIMESTAMP)
    end_datetime: Mapped[datetime] = mapped_column(TIMESTAMP)

    variant: Mapped["Variant"] = relationship(back_populates="result_info")
