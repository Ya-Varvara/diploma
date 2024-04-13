from datetime import datetime

from pydantic import BaseModel


class VariantResultInfoBase(BaseModel):
    variant_id: int
    students_name: str
    students_surname: str
    start_datetime: datetime
    end_datetime: datetime


class VariantResultInfoCreate(VariantResultInfoBase):
    pass


class VariantResultInfo(VariantResultInfoBase):
    id: int
