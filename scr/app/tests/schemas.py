from typing import Optional, List, Any

from pydantic import BaseModel, ConfigDict


class TestBase(BaseModel):
    """
    Модель Тест
    """
    name: str
    user_id: int
    description: dict[str, Any]
    link: str

class TestCreate(TestBase):
    pass

class TestUpdate(TestCreate):
    pass

class TestUpdatePartial(TestCreate):
    name: Optional[str] = None
    user_id: Optional[int] = None
    description: Optional[dict[str, Any]] = None
    link: Optional[str] = None

class Test(TestBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
