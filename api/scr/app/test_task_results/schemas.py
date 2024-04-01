from typing import Optional, List, Any
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StudentsData(BaseModel):
    """
    Модель для отображения данных о студенте.
    """

    name: str
    surname: str


class AnswerData(BaseModel):
    """
    Модель для отображения выбранного результата.
    """

    data: str


class TestTaskResultBase(BaseModel):
    """
    Модель Результат выполнения задания
    """

    test_task_id: int
    answer: AnswerData
    data: Optional[bytes]


# class TestTaskResultCreate(TestTaskResultBase):
#     pass


# class TestTaskResultUpdate(TestTaskResultCreate):
#     pass


# class TestTaskResultUpdatePartial(TestTaskResultCreate):
#     test_task_id: Optional[int] = None
#     answer: Optional[dict[str, Any]] = None
#     data: Optional[bytes] = None


class TestTaskResult(TestTaskResultBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
