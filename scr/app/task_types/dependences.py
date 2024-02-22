from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from scr.app.database import get_async_session

from scr.app.core.models import TaskType

import scr.app.task_types.crud as crud


async def task_type_by_id(
    task_type_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> TaskType:
    task_type = await crud.get_task_type(session=session, task_type_id=task_type_id)
    if task_type is not None:
        return task_type

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task type {task_type_id} not found!",
    )
