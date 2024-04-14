from typing import Optional, List, Any, Dict
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from api.scr.app.tests.schemas import TestDataForVariant
from api.scr.app.tasks.schemas import TaskForStudent, FullTask
from api.scr.app.uploaded_files.schemas import UploadedFile
from api.scr.app.variant_result_info.schemas import VariantResultInfo
from api.scr.app.variant_task.schemas import (
    VariantTaskForTeacher,
    VariantTaskForStudent,
)
from api.scr.app.variant_result_info.schemas import VariantResultInfoCreate
from api.scr.app.variants_task_result.schemas import VariantTaskResultCreate


class VariantBase(BaseModel):
    """
    Модель для варианта задания
    """

    variant: int
    test_id: int
    is_given: bool = False


class VariantForStudent(BaseModel):
    id: int
    variant: int
    test_info: TestDataForVariant
    tasks: List[VariantTaskForStudent]


class VariantForTeacher(BaseModel):
    id: int
    variant: int
    test_info: TestDataForVariant

    tasks: List[VariantTaskForTeacher]

    variant_result_info: Optional[VariantResultInfo]
    uploaded_file: Optional[UploadedFile]

    is_given: bool


class VariantResultCreate(BaseModel):
    info: VariantResultInfoCreate
    answers: List[VariantTaskResultCreate]
