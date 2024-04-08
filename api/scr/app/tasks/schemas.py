from typing import Optional, List, Any, Dict
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from api.scr.app.task_types.schemas import FullTaskType


class TaskBase(BaseModel):
    """
    Базовая модель задание теста

    На основе этой модели делаются модели для получения и изменения задания
    """

    name: str
    type_id: int
    description_data: Optional[str]
    condition_data: Dict[str, Any]


class TaskForStudent(TaskBase):
    """
    Модель для отправки задания на фронтенд
    """

    type: FullTaskType


class TaskCreate(TaskBase):
    """
    Модель для создания задания. Задание создается на сервере или в будущей экспортируется из файла, поэтому эта модель не отправляется на фронтенд.
    """

    answer_data: Dict[str, Any]


class TaskUpdate(TaskCreate):
    """
    Модель для изменения задания
    """

    answer_data: Optional[Dict[str, Any]]


class TaskUpdatePartial(TaskBase):
    """
    Модель для частичного изменения задания
    """

    name: Optional[str]
    type_id: Optional[int]
    description_data: Optional[str]
    condition_data: Optional[Dict[str, Any]]
    answer_data: Optional[Dict[str, Any]]


class Task(TaskCreate):
    """
    Полная модель задания
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool


class FullTask(Task):
    type: FullTaskType
