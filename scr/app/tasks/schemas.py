from typing import Optional, List

from pydantic import BaseModel

class TastTypeCreate(BaseModel):
    """Base TastType model."""

    id: int
    name: str
    data_types: List[str]
    answer_type: List[str]
