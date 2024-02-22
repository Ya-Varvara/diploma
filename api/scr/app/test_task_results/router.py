from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.database import get_async_session
from api.scr.app.test_task_results.schemas import (
    TestTaskResultCreate,
    TestTaskResultUpdate,
    TestTaskResultUpdatePartial,
    TestTaskResult,
)
from api.scr.app.test_task_results.dependences import test_task_result_by_id

import api.scr.app.test_task_results.crud as crud

router = APIRouter(prefix="/test_task_result", tags=["TestTaskResult"])


@router.get("/", response_model=list[TestTaskResult])
async def get_test_task_results(session: AsyncSession = Depends(get_async_session)):
    return await crud.get_test_task_results(session=session)


@router.post(
    "/",
    response_model=TestTaskResult,
    status_code=status.HTTP_201_CREATED,
)
async def create_test_task_result(
    test_task_result_in: TestTaskResultCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.create_test_task_result(
        session=session, test_task_result_in=test_task_result_in
    )


@router.get("/{test_task_result_id}/", response_model=TestTaskResult)
async def get_test_task_result(
    test_task_result: TestTaskResult = Depends(test_task_result_by_id),
):
    return test_task_result


@router.put("/{test_task_result_id}/")
async def update_test_task_result(
    test_task_result_update: TestTaskResultUpdate,
    test_task_result: TestTaskResult = Depends(test_task_result_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.update_test_task_result(
        session=session,
        test_task_result=test_task_result,
        test_task_result_update=test_task_result_update,
    )


@router.patch("/{test_task_result_id}/")
async def update_test_task_result_partial(
    test_task_result_update: TestTaskResultUpdatePartial,
    test_task_result: TestTaskResult = Depends(test_task_result_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.update_test_task_result(
        session=session,
        test_task_result=test_task_result,
        test_task_result_update=test_task_result_update,
        partial=True,
    )


@router.delete("/{test_task_result_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_task_result(
    test_task_result: TestTaskResult = Depends(test_task_result_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await crud.delete_test_task_result(
        session=session, test_task_result=test_task_result
    )
