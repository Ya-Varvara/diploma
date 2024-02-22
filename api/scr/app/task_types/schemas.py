from typing import Optional, List, Any

from pydantic import BaseModel, ConfigDict


class TaskTypeBase(BaseModel):
    """
    Модель Тип задания
    """

    name: str
    data_types: List[str]
    answer_type: List[str]


class TaskTypeCreate(TaskTypeBase):
    pass


class TaskTypeUpdate(TaskTypeCreate):
    pass


class TaskTypeUpdatePartial(TaskTypeCreate):
    name: Optional[str] = None
    data_types: Optional[List[str]] = None
    answer_type: Optional[List[str]] = None


class TaskType(TaskTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
