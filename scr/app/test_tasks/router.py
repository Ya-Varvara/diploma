from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from scr.app.database import get_async_session
from scr.app.test_tasks.schemas import (
    TestTaskCreate,
    TestTaskUpdate,
    TestTaskUpdatePartial,
    TestTask,
)
from scr.app.test_tasks.dependences import test_task_by_id

import scr.app.test_tasks.crud as crud

router = APIRouter(prefix="/test_task", tags=["TestTask"])


@router.get("/", response_model=list[TestTask])
async def get_test_tasks(session: AsyncSession = Depends(get_async_session)):
    return await crud.get_test_tasks(session=session)


# @router.post(
#     "/",
#     response_model=TestTask,
#     status_code=status.HTTP_201_CREATED,
# )
async def create_test_task(
    test_task_in: TestTaskCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.create_test_task(session=session, test_task_in=test_task_in)


# @router.get("/{test_task_id}/", response_model=TestTask)
async def get_test_task(test_task: TestTask = Depends(test_task_by_id)):
    return test_task


# @router.put("/{test_task_id}/")
async def update_test_task(
    test_task_update: TestTaskUpdate,
    test_task: TestTask = Depends(test_task_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.update_test_task(
        session=session, test_task=test_task, test_task_update=test_task_update
    )


# @router.patch("/{test_task_id}/")
async def update_test_task_partial(
    test_task_update: TestTaskUpdatePartial,
    test_task: TestTask = Depends(test_task_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.update_test_task(
        session=session,
        test_task=test_task,
        test_task_update=test_task_update,
        partial=True,
    )


# @router.delete("/{test_task_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_task(
    test_task: TestTask = Depends(test_task_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await crud.delete_test_task(session=session, test_task=test_task)
