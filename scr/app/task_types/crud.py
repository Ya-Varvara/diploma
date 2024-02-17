"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from scr.app.core.models import TaskType

from scr.app.task_types.schemas import TaskTypeCreate, TaskTypeUpdate, TaskTypeUpdatePartial


async def get_task_types(session: AsyncSession) -> list[TaskType]:
    stmt = select(TaskType).order_by(TaskType.id)
    result: Result = await session.execute(stmt)
    task_types = result.scalars().all()
    return list(task_types)


async def get_task_type(session: AsyncSession, task_type_id: int) -> TaskType | None:
    return await session.get(TaskType, task_type_id)


async def create_task_type(session: AsyncSession, task_type_in: TaskTypeCreate) -> TaskType:
    task_type = TaskType(**task_type_in.model_dump())
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