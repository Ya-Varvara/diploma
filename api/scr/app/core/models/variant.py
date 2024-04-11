from typing import TYPE_CHECKING, List

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .test import Test
    from .uploaded_file import UploadedFile
    from .variant_result_info import VariantResultInfo
    from .variant_task import VariantTask


class Variant(Base):
    __tablename__ = "variants"

    variant: Mapped[int]
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"))
    is_given: Mapped[bool]

    test: Mapped["Test"] = relationship(back_populates="variants")
    tasks: Mapped[List["VariantTask"]] = relationship(back_populates="variant")
    result_info: Mapped["VariantResultInfo"] = relationship(back_populates="variant")
    uploaded_file: Mapped["UploadedFile"] = relationship(back_populates="variant")
