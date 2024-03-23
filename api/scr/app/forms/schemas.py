from typing import Optional, List, Any, Dict
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Form(BaseModel):
    """
    Базовая модель для формы
    Вызывается с интерфейса, когда пользователь выбирает тип задания при создании тестирования
    """

    id: int
    name: str
    short_name: str
    condition_form: bool
    answer_form: bool
