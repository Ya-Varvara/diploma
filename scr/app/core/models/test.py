from typing import List, Any, Dict, TYPE_CHECKING

from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Column, Integer, Text, String, Boolean, MetaData, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Test(Base):
    __tablename__ = "tests"

    name: Mapped[str] = mapped_column(String(64))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    description: Mapped[Dict[str, Any]] = mapped_column(JSONB)
    link: Mapped[str] = mapped_column(String(64))

    user: Mapped["User"] = relationship(back_populates="tests")
