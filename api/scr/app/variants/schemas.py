from typing import Optional, List, Any, Dict
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from api.scr.app.tests.schemas import TestDataForVariant
from api.scr.app.tasks.schemas import TaskForStudent, FullTask
from api.scr.app.uploaded_files.schemas import UploadedFile
from api.scr.app.variant_result_info.schemas import VariantResultInfo


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
    tasks: List[TaskForStudent]


class VariantForTeacher(BaseModel):
    id: int
    variant: int
    test_info: TestDataForVariant

    tasks: List[FullTask]

    variant_result_info: Optional[VariantResultInfo]
    uploaded_file: Optional[UploadedFile]

    is_given: bool
