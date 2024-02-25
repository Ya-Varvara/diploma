from typing import Optional

from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate


class UserRead(BaseUser[int]):
    """Base User model."""

    id: int
    username: str
    email: str
    # meta: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    # if PYDANTIC_V2:  # pragma: no cover
    #     model_config = ConfigDict(from_attributes=True)  # type: ignore
    # else:  # pragma: no cover

    class Config:
        orm_mode = True


class UserCreate(BaseUserCreate):
    id: int
    username: str
    email: str
    # meta: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(BaseUserUpdate):
    password: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
