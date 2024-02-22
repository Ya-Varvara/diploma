from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from scr.app.database import get_async_session

from scr.app.auth.router import get_current_user

from scr.app.tasks.schemas import TaskCreate, TaskUpdate, TaskUpdatePartial, Task
from scr.app.tasks.dependences import task_by_id

from scr.app.core.models import User

import scr.app.tasks.crud as crud

router = APIRouter(prefix="/task", tags=["Task"])


@router.get("/", response_model=list[Task])
async def get_tasks(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user()),
):
    options = {"user_id": user.id}
    return await crud.get_tasks(session=session, options=options)


@router.post(
    "/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user()),
):
    return await crud.create_task(session=session, task_in=task_in, user_id=user.id)


@router.get("/{task_id}/", response_model=Task)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user()),
):
    options = {"user_id": user.id}
    task = crud.get_task(session=session, task_id=task_id, options=options)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task not found",
        )
    return task


@router.put("/{task_id}/")
async def update_task(
    task_update: TaskUpdate,
    task: Task = Depends(task_by_id),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user()),
):
    if task.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task not yours",
        )
    return await crud.update_task(session=session, task=task, task_update=task_update)


@router.patch("/{task_id}/")
async def update_task_partial(
    task_update: TaskUpdatePartial,
    task: Task = Depends(task_by_id),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user()),
):
    if task.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task not yours",
        )
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
    user: User = Depends(get_current_user()),
) -> None:
    if task.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task not yours",
        )
    await crud.delete_task(session=session, task=task)
