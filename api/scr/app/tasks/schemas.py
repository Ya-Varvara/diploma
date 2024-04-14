from typing import Optional, Any, Dict
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


class TaskCreate(TaskBase):
    """
    Модель для создания задания. Задание создается на сервере или в будущей экспортируется из файла, поэтому эта модель не отправляется на фронтенд.
    """

    answer_data: Dict[str, Any]


class TaskForStudent(TaskBase):
    """
    Модель для отправки задания на фронтенд студенту
    """

    id: int
    type: FullTaskType


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
