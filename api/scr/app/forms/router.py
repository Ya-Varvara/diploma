from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.database import get_async_session
from api.scr.app.forms import schemas as sch
from api.scr.app.core.models import User

from api.scr.app.auth.router import get_current_user
from api.scr.app.forms import crud


router = APIRouter(prefix="/forms", tags=["Forms"])


@router.get("/", response_model=list[sch.Form])
async def get_all_forms(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user()),
):
    return await crud.get_all_forms(session=session)
