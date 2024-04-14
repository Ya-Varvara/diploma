from typing import Any, Dict

from pydantic import BaseModel


class VariantTaskResultBase(BaseModel):
    """
    Базовая модель ответа на задание варианта
    """

    variants_task_id: int
    answer: Dict[str, Any]


class VariantTaskResultCreate(VariantTaskResultBase):
    pass


class VariantTaskResult(VariantTaskResultBase):
    id: int
    is_correct: bool
