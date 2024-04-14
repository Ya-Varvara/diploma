"""
Create
Read
Update
Delete
"""

from datetime import datetime
from typing import List
import logging

from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.forms import crud as fcrud

from api.scr.app.task_types.schemas import TaskTypeCreate, TaskTypeUpdate

from api.scr.app.task_types.handlers import make_new_task_type_data


logger = logging.getLogger(__name__)


async def get_all_base_task_types(session: AsyncSession) -> List[dbm.BaseTaskType]:
    logger.debug(f"CRUD Getting all base task types...")
    
    stmt = select(dbm.BaseTaskType)
    result: Result = await session.execute(stmt)
    base_task_types = result.scalars().all()

    logger.debug(f"CRUD Base task types were found: {base_task_types}")
    return list(base_task_types)


async def get_all_task_types(session: AsyncSession, **options) -> List[dbm.TaskType]:
    logger.debug(f"CRUD Getting all task types...")

    stmt = (
        select(dbm.TaskType)
        .options(
            joinedload(dbm.TaskType.condition_forms),
            joinedload(dbm.TaskType.answer_forms),
            joinedload(dbm.TaskType.base_type),
        )
        .where(dbm.TaskType.deleted == False)
        .order_by(dbm.TaskType.id)
    )
    if user_id := options.get("user_id", ""):
        stmt = stmt.where(dbm.TaskType.user_id == user_id)
    result: Result = await session.execute(stmt)
    task_types = result.scalars().unique().all()

    logger.debug(f"CRUD Task types were found: {task_types}")
    return list(task_types)


async def get_task_type_by_id(
    session: AsyncSession, task_type_id: int, **options
) -> dbm.TaskType | None:
    logger.debug(f"CRUD Getting task type by id={task_type_id}...")

    stmt = (
        select(dbm.TaskType)
        .options(
            joinedload(dbm.TaskType.tasks),
            joinedload(dbm.TaskType.condition_forms),
            joinedload(dbm.TaskType.answer_forms),
            joinedload(dbm.TaskType.base_type),
        )
        .where(dbm.TaskType.id == task_type_id)
        .where(dbm.TaskType.deleted == False)
    )

    if user_id := options.get("user_id", ""):
        stmt = stmt.where(dbm.TaskType.user_id == user_id)

    task_type: dbm.TaskType | None = await session.scalar(stmt)

    logger.debug(f"CRUD Task type was found: {task_type}")
    return task_type


async def get_task_type_by_name(
    session: AsyncSession, task_type_name: str, **options
) -> dbm.TaskType | None:
    logger.debug(f"CRUD Getting task type by name={task_type_name}...")
    stmt = (
        select(dbm.TaskType)
        .options(
            joinedload(dbm.TaskType.tasks),
            joinedload(dbm.TaskType.condition_forms),
            joinedload(dbm.TaskType.answer_forms),
            joinedload(dbm.TaskType.base_type),
        )
        .where(dbm.TaskType.name == task_type_name)
        .where(dbm.TaskType.deleted == False)
    )

    if user_id := options.get("user_id", ""):
        stmt = stmt.where(dbm.TaskType.user_id == user_id)

    task_type: dbm.TaskType | None = await session.scalar(stmt)
    logger.debug(f"CRUD Task type was found: {task_type}")
    return task_type


async def create_task_type(
    session: AsyncSession, task_type_in: TaskTypeCreate, user_id: int
) -> dbm.TaskType:
    logger.debug(f"CRUD Task type creation...")
    task_type = make_new_task_type_data(task_type_in, user_id)
    session.add(task_type)
    await session.flush()
    
    logger.debug(f"CRUD Task type was created with id={task_type.id}")

    await fcrud.create_answer_forms(session, task_type_in.answer_forms, task_type.id)
    await fcrud.create_condition_forms(
        session, task_type_in.condition_forms, task_type.id
    )
    await session.refresh(task_type)
    return task_type


async def update_task_type(
    session: AsyncSession,
    task_type: dbm.TaskType,
    task_type_update: TaskTypeUpdate,
    partial: bool = False,
) -> dbm.TaskType:
    logger.debug(f"CRUD Task type update...")
    for name, value in task_type_update.model_dump(
        exclude_unset=partial, exclude={"condition_forms", "answer_forms"}
    ).items():
        setattr(task_type, name, value)

    setattr(task_type, "updated_at", datetime.now())
    await session.commit()

    if task_type_update.condition_forms:
        await fcrud.update_condition_forms(
            session, task_type_update.condition_forms, task_type.id
        )

    if task_type_update.answer_forms:
        await fcrud.update_answer_forms(
            session, task_type_update.answer_forms, task_type.id
        )

    return task_type


async def delete_task_type(
    session: AsyncSession,
    task_type: dbm.TaskType,
) -> None:
    logger.debug(f"CRUD Task type delete...")
    setattr(task_type, "updated_at", datetime.now())
    setattr(task_type, "deleted", True)
    await session.commit()
