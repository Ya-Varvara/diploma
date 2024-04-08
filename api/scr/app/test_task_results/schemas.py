from typing import Optional, List, Any
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from api.scr.app.tasks.schemas import FullTask


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

    type: str
    data: Any


class TimeData(BaseModel):
    """ """

    start_time: datetime
    end_time: datetime


class TestTaskResultBase(BaseModel):
    """
    Модель Результат выполнения задания
    """

    test_task_id: int
    answer: AnswerData
    students_info: StudentsData
    time_data: TimeData


class TestTaskResultCreate(TestTaskResultBase):
    pass


# class TestTaskResultUpdate(TestTaskResultCreate):
#     pass


# class  TestTaskResultUpdatePartial(TestTaskResultCreate):
#     test_task_id: Optional[int] = None
#     answer: Optional[dict[str, Any]] = None
#     data: Optional[bytes] = None


class TestTaskResult(TestTaskResultBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_correct: Optional[bool]


class FullTestTaskResult(TestTaskResult):
    """ """

    task: FullTask
