from typing import TYPE_CHECKING, Optional, List, Any
from datetime import datetime, time

from pydantic import BaseModel, ConfigDict

from api.scr.app.tasks.schemas import TaskForStudent

from api.scr.app.task_types.schemas import FullTaskType


class UploadedFileBase(BaseModel):
    """
    Базовая модель для таблицы с файлами
    """

    name: str
    path: str
    upload_date: datetime
    test_task_id: int


class UploadedFileCreation(BaseModel):
    """
    Базовая модель для добавления данных в таблицу с файлами
    """

    name: str
    path: str
    test_task_id: int


class UploadedFile(UploadedFileBase):
    """
    Модель для таблицы с файлами
    """

    id: int
