from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from scr.app.database import get_async_session

from scr.app.core.models import Task

import scr.app.tasks.crud as crud


async def task_by_id(
    task_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> Task:
    task = await crud.get_task(session=session, task_id=task_id)
    if task is not None:
        return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found!",
    )