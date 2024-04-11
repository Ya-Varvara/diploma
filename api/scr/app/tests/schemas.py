from typing import TYPE_CHECKING, Optional, List, Any
from datetime import datetime, time

from pydantic import BaseModel, ConfigDict

from api.scr.app.tasks.schemas import TaskForStudent

from api.scr.app.task_types.schemas import FullTaskType


class TestBase(BaseModel):
    """
    Базовая модель теста
    """

    name: str
    start_datetime: datetime
    end_datetime: datetime
    test_time: time
    variants_number: int
    upload: bool


class TaskTypesForTestCreation(BaseModel):
    """
    Модель для описания типов заданий в интерфейсе. Нужно указать ID типа и количество заданий.
    """

    type_id: int
    number: int


class TaskTypesForFullTest(BaseModel):
    """
    Модель для описания типов заданий в интерфейсе. Нужно указать ID типа и количество заданий.
    """

    type: FullTaskType
    number: int


class TestCreate(TestBase):
    """
    Модель для создания теста. Используется для создания нового тестирования пользователем в интерфейсе.
    """

    task_types: List[TaskTypesForTestCreation]


class TestUpdate(TestCreate):
    pass


class TestUpdatePartial(TestCreate):
    name: Optional[str]
    start_datetime: Optional[datetime]
    end_datetime: Optional[datetime]
    test_time: Optional[time]
    variants_number: Optional[int]
    task_types: Optional[List[TaskTypesForTestCreation]]


class Test(TestBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    link: str
    created_at: datetime
    updated_at: datetime
    deleted: bool


class FullTest(Test):
    task_types: List[TaskTypesForFullTest]


class TestVariant(BaseModel):
    """
    Модель для отображения варианта теста в интерфейсе для студентов.
    """

    name: str
    start_datetime: datetime
    end_datetime: datetime
    test_time: time
    variant_number: int
    tasks: List[TaskForStudent]
    upload: bool


class TestDataForVariant(BaseModel):
    """
    Модель для отображения информации о варианте для студента.
    """

    name: str
    start_datetime: datetime
    end_datetime: datetime
    test_time: time
    upload: bool
