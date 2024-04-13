from typing import Any, Dict
from datetime import datetime

from pydantic import BaseModel


class UploadedFileBase(BaseModel):
    """ """

    name: str
    path: str
    variant_id: int


class UploadedFileCreate(UploadedFileBase):
    pass


class UploadedFile(UploadedFileBase):
    id: int
    uploaded_date: datetime
