from typing import Optional, List, Any

from pydantic import BaseModel, ConfigDict


class TestTaskResultBase(BaseModel):
    """
    Модель Результат выполнения задания
    """

    test_task_id: int
    answer: dict[str, Any]
    data: bytes


class TestTaskResultCreate(TestTaskResultBase):
    pass


class TestTaskResultUpdate(TestTaskResultCreate):
    pass


class TestTaskResultUpdatePartial(TestTaskResultCreate):
    test_task_id: Optional[int] = None
    answer: Optional[dict[str, Any]] = None
    data: Optional[bytes] = None


class TestTaskResult(TestTaskResultBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
