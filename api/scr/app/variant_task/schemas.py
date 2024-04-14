from typing import Any, Dict, Optional

from pydantic import BaseModel

from api.scr.app.tasks.schemas import FullTask, TaskForStudent
from api.scr.app.variants_task_result.schemas import VariantTaskResult


class VariantTaskBase(BaseModel):
    """
    Базовая модель ответа на задание варианта
    """

    variant_id: int
    task_id: int


class VariantTaskCreate(VariantTaskBase):
    pass


class VariantTaskForStudent(VariantTaskBase):
    id: int
    task: TaskForStudent


class VariantTaskForTeacher(VariantTaskForStudent):
    task: FullTask
    students_result: Optional[VariantTaskResult]
