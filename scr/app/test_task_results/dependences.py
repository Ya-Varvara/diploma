from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from scr.app.database import get_async_session

from scr.app.core.models import TestTaskResult

import scr.app.test_task_results.crud as crud


async def test_task_result_by_id(
    test_task_result_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> TestTaskResult:
    test_task_result = await crud.get_test_task_result(
        session=session, test_task_result_id=test_task_result_id
    )
    if test_task_result is not None:
        return test_task_result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"TestTaskResult {test_task_result_id} not found!",
    )
