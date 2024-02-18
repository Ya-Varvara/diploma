from typing import Optional, List, Any

from pydantic import BaseModel, ConfigDict


class TestTaskBase(BaseModel):
    """
    Модель Вариант теста
    """

    variant: int
    test_id: int
    task_id: int
    is_given: bool = False


class TestTaskCreate(TestTaskBase):
    pass


class TestTaskUpdate(TestTaskCreate):
    pass


class TestTaskUpdatePartial(TestTaskCreate):
    variant: Optional[int] = None
    test_id: Optional[int] = None
    task_id: Optional[int] = None
    is_given: Optional[bool] = None


class TestTask(TestTaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
