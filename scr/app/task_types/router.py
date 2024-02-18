from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from scr.app.database import get_async_session
from scr.app.task_types.schemas import (
    TaskTypeCreate,
    TaskTypeUpdate,
    TaskTypeUpdatePartial,
    TaskType,
)
from scr.app.task_types.dependences import task_type_by_id

import scr.app.task_types.crud as crud

router = APIRouter(prefix="/task_type", tags=["Task type"])


@router.get("/", response_model=list[TaskType])
async def get_task_types(session: AsyncSession = Depends(get_async_session)):
    return await crud.get_task_types(session=session)


@router.post(
    "/",
    response_model=TaskType,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_type(
    task_type_in: TaskTypeCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.create_task_type(session=session, task_type_in=task_type_in)


@router.get("/{task_type_id}/", response_model=TaskType)
async def get_task_type(task_type: TaskType = Depends(task_type_by_id)):
    return task_type


@router.put("/{task_type_id}/")
async def update_task_type(
    task_type_update: TaskTypeUpdate,
    task_type: TaskType = Depends(task_type_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.update_task_type(
        session=session, task_type=task_type, task_type_update=task_type_update
    )


@router.patch("/{task_type_id}/")
async def update_task_type_partial(
    task_type_update: TaskTypeUpdatePartial,
    task_type: TaskType = Depends(task_type_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.update_task_type(
        session=session,
        task_type=task_type,
        task_type_update=task_type_update,
        partial=True,
    )


@router.delete("/{task_type_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_type(
    task_type: TaskType = Depends(task_type_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await crud.delete_task_type(session=session, task_type=task_type)
