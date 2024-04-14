from typing import Optional
import logging
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from api.scr.app.auth.db_handlers import get_user_db
from api.scr.app.core.models import User


SECRET = "SECRET"


logger = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
