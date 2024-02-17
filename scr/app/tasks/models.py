from typing import List

from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Column, Integer, Text, String, Boolean, JSON, MetaData, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

Base: DeclarativeMeta = declarative_base()


class TaskType(Base):
    __tablename__ = "task_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    data_types: Mapped[List[str]] = mapped_column(ARRAY(String))
    answer_type: Mapped[List[str]] = mapped_column(ARRAY(String))

