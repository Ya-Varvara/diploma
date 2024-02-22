"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from api.scr.app.core.models import TestTask

from api.scr.app.test_tasks.schemas import (
    TestTaskCreate,
    TestTaskUpdate,
    TestTaskUpdatePartial,
)


async def get_test_tasks(session: AsyncSession) -> list[TestTask]:
    stmt = select(TestTask).order_by(TestTask.id)
    result: Result = await session.execute(stmt)
    test_tasks = result.scalars().all()
    return list(test_tasks)


async def get_test_task(session: AsyncSession, test_task_id: int) -> TestTask | None:
    return await session.get(TestTask, test_task_id)


async def create_test_task(
    session: AsyncSession, test_task_in: TestTaskCreate
) -> TestTask:
    test_task = TestTask(**test_task_in.model_dump())
    session.add(test_task)
    await session.commit()
    # await session.refresh(product)
    return test_task


async def update_test_task(
    session: AsyncSession,
    test_task: TestTask,
    test_task_update: TestTaskUpdate | TestTaskUpdatePartial,
    partial: bool = False,
) -> TestTask:
    for name, value in test_task_update.model_dump(exclude_unset=partial).items():
        setattr(test_task, name, value)
    await session.commit()
    return test_task


async def delete_test_task(
    session: AsyncSession,
    test_task: TestTask,
) -> None:
    await session.delete(test_task)
    await session.commit()
