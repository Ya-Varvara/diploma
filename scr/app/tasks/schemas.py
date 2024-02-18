from typing import Optional, List, Any

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    """
    Модель Задание
    """

    name: str
    type_id: int
    data: dict[str, Any]


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskCreate):
    pass


class TaskUpdatePartial(TaskCreate):
    name: Optional[str] = None
    type: Optional[int] = None
    data: Optional[dict[str, Any]] = None


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
