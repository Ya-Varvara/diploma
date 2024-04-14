from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.database import get_async_session

from api.scr.app.auth.router import get_current_user

from api.scr.app.core.models import User

import api.scr.app.tasks.crud as crud

router = APIRouter(prefix="/task", tags=["Task"])
