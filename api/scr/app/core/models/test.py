from typing import Any, Dict, TYPE_CHECKING

from sqlalchemy import (
    String,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .test_task import TestTask


class Test(Base):
    __tablename__ = "tests"

    name: Mapped[str] = mapped_column(String(64))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    description: Mapped[Dict[str, Any]] = mapped_column(JSONB)
    link: Mapped[str] = mapped_column(String(64))

    user: Mapped["User"] = relationship(back_populates="tests")
    test_variants: Mapped[list["TestTask"]] = relationship(back_populates="test")
