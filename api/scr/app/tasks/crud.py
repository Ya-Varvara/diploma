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
from api.scr.app.core import models as dbm

from api.scr.app.tasks.schemas import TaskCreate, TaskUpdate, TaskUpdatePartial


# async def get_tasks(session: AsyncSession, **options) -> list[Task]:
#     stmt = select(Task).options(joinedload(Task.type)).order_by(Task.id)
#     if user_id := options.get("user_id", ""):
#         stmt = stmt.where(Task.user_id == user_id)
#     result: Result = await session.execute(stmt)
#     tasks = result.scalars().all()
#     return list(tasks)


async def get_task_by_id(session: AsyncSession, task_id: int) -> dbm.Task | None:
    stmt = (
        select(dbm.Task)
        .options(
            joinedload(dbm.Task.type),
            joinedload(dbm.Task.type, dbm.TaskType.answer_forms),
            joinedload(dbm.Task.type, dbm.TaskType.condition_forms),
            joinedload(dbm.Task.type, dbm.TaskType.base_type),
        )
        .where(dbm.Task.id == task_id)
    )
    task: dbm.Task | None = await session.scalar(stmt)
    return task


# async def get_task_by_name(
#     session: AsyncSession, task_name: str, **options
# ) -> Task | None:
#     stmt = (
#         select(Task).where(Task.name == task_name).options(joinedload(Task.type))
#     )
#     if user_id := options.get("user_id", ""):
#         stmt = stmt.where(Task.user_id == user_id)
#     result: Result = await session.execute(stmt)
#     task: Task = result.one_or_none()
#     return task


# async def create_task(session: AsyncSession, task_in: TaskCreate, user_id: int) -> Task:
#     task = Task(**task_in.model_dump())
#     task.user_id = user_id
#     session.add(task)
#     await session.commit()
#     # await session.refresh(product)
#     return task


# async def update_task(
#     session: AsyncSession,
#     task: Task,
#     task_update: TaskUpdate | TaskUpdatePartial,
#     partial: bool = False,
# ) -> Task:
#     for name, value in task_update.model_dump(exclude_unset=partial).items():
#         setattr(task, name, value)
#     await session.commit()
#     return task


# async def delete_task(
#     session: AsyncSession,
#     task: Task,
# ) -> None:
#     await session.delete(task)
#     await session.commit()
