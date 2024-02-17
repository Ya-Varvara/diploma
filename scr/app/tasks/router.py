from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from scr.app.database import get_async_session
from scr.app.tasks.schemas import TaskCreate, TaskUpdate, TaskUpdatePartial, Task
from scr.app.tasks.dependences import task_by_id

import scr.app.tasks.crud as crud

router = APIRouter(
    prefix="/task",
    tags=["Task"]
)


@router.get("/", response_model=list[Task])
async def get_tasks(session: AsyncSession = Depends(get_async_session)):
    return await crud.get_tasks(session=session)


@router.post(
    "/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.create_task(session=session, task_in=task_in)


@router.get("/{task_id}/", response_model=Task)
async def get_task(task: Task = Depends(task_by_id)):
    return task


@router.put("/{task_id}/")
async def update_task(
    task_update: TaskUpdate,
    task: Task = Depends(task_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.update_task(
        session=session,
        task=task,
        task_update=task_update
    )


@router.patch("/{task_id}/")
async def update_task_partial(
    task_update: TaskUpdatePartial,
    task: Task = Depends(task_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.update_task(
        session=session,
        task=task,
        task_update=task_update,
        partial=True,
    )


@router.delete("/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task: Task = Depends(task_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await crud.delete_task(session=session, task=task)
