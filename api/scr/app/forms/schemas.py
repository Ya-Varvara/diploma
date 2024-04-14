from pydantic import BaseModel, ConfigDict


class Form(BaseModel):
    """
    Базовая модель для формы
    Вызывается с интерфейса, когда пользователь выбирает тип задания при создании тестирования
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    short_name: str
    condition_form: bool
    answer_form: bool
