from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.database import get_async_session

import api.scr.app.test_task_results.crud as crud

from api.scr.app.core import models as dbm
from api.scr.app.test_task_results import schemas as sch
from api.scr.app.auth.router import get_current_user


router = APIRouter(prefix="/test_task_result", tags=["TestTaskResult"])


@router.get("/", response_model=list[sch.FullTestTaskResult])
async def get_test_task_results(
    test_id: int,
    variant: int,
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
):
    return await crud.get_test_task_results(
        session=session, test_id=test_id, variant=variant
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_test_task_results(
    test_task_result_in: List[sch.TestTaskResultCreate],
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.create_test_task_results(
        session=session, test_task_results_in=test_task_result_in
    )
