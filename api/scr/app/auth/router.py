from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from api.scr.app.auth.schemas import UserRead, UserCreate, UserUpdate
from api.scr.app.auth.manager import get_user_manager
from api.scr.app.auth.auth import auth_backend
from api.scr.app.core.models import User


router = APIRouter(prefix="/auth", tags=["Auth"])

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))


def get_current_user():
    return fastapi_users.current_user()
