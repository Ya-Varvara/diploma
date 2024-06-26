from typing import Optional, List, Any, Dict
from datetime import datetime

from pydantic import BaseModel

from api.scr.app.forms.schemas import Form


class BaseTaskType(BaseModel):
    """
    Модель для базового типа задания.
    Используется только для получения данных.

    Пользователь не может изменить или удалить базовый тип
    """

    id: int
    name: str
    settings: Dict[str, Any]


class TaskTypeBase(BaseModel):
    """
    Базовая модель для типа задания

    На основе этой модели делаются модели для получения и изменения типа задания
    """

    name: str
    base_task_type: Optional[int] = None
    settings: Optional[Dict[str, Any]] = None
    condition_forms: List[int]
    answer_forms: List[int]


class TaskTypeCreate(TaskTypeBase):
    pass


class TaskTypeUpdate(BaseModel):
    """ """

    name: Optional[str] = None
    base_task_type: Optional[int] = None
    settings: Optional[Dict[str, Any]] = None
    condition_forms: Optional[List[int]] = None
    answer_forms: Optional[List[int]] = None


class TaskType(TaskTypeBase):
    """
    Модель типа задания. Используется для получения полной информации о типе
    """

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool


class FullTaskType(TaskType):
    condition_forms: List[Form]
    answer_forms: List[Form]
