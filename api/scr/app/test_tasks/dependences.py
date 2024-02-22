from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.database import get_async_session

from api.scr.app.core.models import TestTask

import api.scr.app.test_tasks.crud as crud


async def test_task_by_id(
    test_task_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> TestTask:
    test_task = await crud.get_test_task(session=session, test_task_id=test_task_id)
    if test_task is not None:
        return test_task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"TestTask {test_task_id} not found!",
    )
