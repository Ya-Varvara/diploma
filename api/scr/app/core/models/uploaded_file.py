from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import (
    String,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .variant import Variant


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    path: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    upload_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    variant_id: Mapped[int] = mapped_column(ForeignKey("variants.id"))

    variant: Mapped["Variant"] = relationship(back_populates="uploaded_file")
