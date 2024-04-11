from typing import Optional, List, Any, Dict
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from api.scr.app.tests.schemas import TestDataForVariant
from api.scr.app.tasks.schemas import TaskForStudent, FullTask
from api.scr.app.upload.schemas import UploadedFile


class ResultInfo(BaseModel):
    students_name: str
    students_surname: str
    start_datetime: datetime
    end_datetime: datetime


# class VariantTaskResult(BaseModel):
#     id: int
#     answer: Dict[str, Any]
#     is_correct: Optional[bool]


class Variant(BaseModel):
    """
    Модель для варианта задания
    """

    id: int
    variant: int
    test_id: int
    is_given: bool = False


class VariantForStudent(BaseModel):
    variant: int
    test_info: TestDataForVariant
    tasks: List[TaskForStudent]


class VariantForTeacher(BaseModel):
    variant: int
    is_given: bool
    test_info: TestDataForVariant
    tasks: List[FullTask]
    result_info: Optional[ResultInfo]
    uploaded_file: Optional[UploadedFile]
