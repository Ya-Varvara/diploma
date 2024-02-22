"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from scr.app.core.models import TaskType

from scr.app.task_types.schemas import (
    TaskTypeCreate,
    TaskTypeUpdate,
    TaskTypeUpdatePartial,
)


async def get_task_types(session: AsyncSession, **options) -> list[TaskType]:
    stmt = select(TaskType).order_by(TaskType.id)
    if user_id := options.get("user_id", ""):
        stmt = stmt.where(TaskType.user_id == user_id)
    result: Result = await session.execute(stmt)
    task_types = result.scalars().all()
    return list(task_types)


async def get_task_type(
    session: AsyncSession, task_type_id: int, **options
) -> TaskType | None:
    stmt = (
        select(TaskType)
        .options(joinedload(TaskType.tasks))
        .where(TaskType.id == task_type_id)
    )
    if user_id := options.get("user_id", ""):
        stmt = stmt.where(TaskType.user_id == user_id)
    task_type: TaskType | None = await session.scalar(stmt)
    return task_type


async def get_task_type_by_name(
    session: AsyncSession, task_type_name: str, **options
) -> TaskType | None:
    stmt = (
        select(TaskType)
        .options(joinedload(TaskType.tasks))
        .where(TaskType.name == task_type_name)
    )
    if user_id := options.get("user_id", ""):
        stmt = stmt.where(TaskType.user_id == user_id)
    task_type: TaskType | None = await session.scalar(stmt)
    return task_type


async def create_task_type(
    session: AsyncSession, task_type_in: TaskTypeCreate, user_id: int
) -> TaskType:
    task_type = TaskType(**task_type_in.model_dump())
    task_type.user_id = user_id
    session.add(task_type)
    await session.commit()
    # await session.refresh(product)
    return task_type


async def update_task_type(
    session: AsyncSession,
    task_type: TaskType,
    task_type_update: TaskTypeUpdate | TaskTypeUpdatePartial,
    partial: bool = False,
) -> TaskType:
    for name, value in task_type_update.model_dump(exclude_unset=partial).items():
        setattr(task_type, name, value)
    await session.commit()
    return task_type


async def delete_task_type(
    session: AsyncSession,
    task_type: TaskType,
) -> None:
    await session.delete(task_type)
    await session.commit()
