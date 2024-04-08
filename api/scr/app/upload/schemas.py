from typing import TYPE_CHECKING, Optional, List, Any
from datetime import datetime, time

from pydantic import BaseModel, ConfigDict

from api.scr.app.tasks.schemas import TaskForStudent

from api.scr.app.task_types.schemas import FullTaskType


class UploadedFilesBase(BaseModel):
    """
    Базовая модель для таблицы с файлами
    """

    name: str
    path: str
    upload_date: datetime
    test_variant_id: int

class UploadedFilesCreation(BaseModel):
    """
    Базовая модель для добавления данных в таблицу с файлами
    """

    name: str
    path: str

class UploadedFiles(UploadedFilesBase):
    """
    Модель для таблицы с файлами
    """

    id: int