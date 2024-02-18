from typing import Optional, List, Any
from datetime import datetime, time

from pydantic import BaseModel, ConfigDict


class DescriptionBase(BaseModel):
    """
    Описание теста
    """

    students_number: int = 1
    description: str = ""
    tasks: dict[str, int]  # tasks = {"task_type_name": count}
    deadline: datetime
    time: time


class TestBase(BaseModel):
    """
    Модель Тест
    """

    name: str
    user_id: int
    description: DescriptionBase
    link: str


class TestCreate(TestBase):
    pass


class TestUpdate(TestCreate):
    pass


class TestUpdatePartial(TestCreate):
    name: Optional[str] = None
    user_id: Optional[int] = None
    description: Optional[DescriptionBase] = None
    link: Optional[str] = None


class Test(TestBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TestOut(TestBase):
    name: str
    user_id: int
    description: dict
    link: str
