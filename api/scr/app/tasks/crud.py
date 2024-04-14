"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from api.scr.app.core import models as dbm


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
