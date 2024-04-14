"""
Create
Read
Update
Delete
"""

from random import choice
from typing import Any, List
from datetime import datetime
import logging

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm

from api.scr.app.tests import schemas as sch
from api.scr.app.tests.handlers import make_new_test_data
from api.scr.app.test_task_types.crud import add_task_type
from api.scr.app.variants.handlers import create_variant_for_test


logger = logging.getLogger(__name__)


async def get_tests(session: AsyncSession, **options) -> list[dbm.Test]:
    stmt = (
        select(dbm.Test)
        .where(dbm.Test.deleted == False)
        .options(
            joinedload(dbm.Test.task_types),
            joinedload(dbm.Test.task_types, dbm.TestTaskType.task_type),
            joinedload(
                dbm.Test.task_types,
                dbm.TestTaskType.task_type,
                dbm.TaskType.answer_forms,
            ),
            joinedload(
                dbm.Test.task_types,
                dbm.TestTaskType.task_type,
                dbm.TaskType.condition_forms,
            ),
            joinedload(
                dbm.Test.task_types, dbm.TestTaskType.task_type, dbm.TaskType.base_type
            ),
        )
        .order_by(dbm.Test.id)
    )

    if user_id := options.get("user_id", ""):
        stmt = stmt.where(dbm.Test.user_id == user_id)
    result: Result = await session.execute(stmt)
    tests = result.scalars().unique().all()
    return list(tests)


async def get_test_by_id(
    session: AsyncSession, test_id: int, user_id: int
) -> dbm.Test | None:
    stmt = (
        select(dbm.Test)
        .options(
            joinedload(dbm.Test.task_types),
            joinedload(dbm.Test.task_types, dbm.TestTaskType.task_type),
            joinedload(
                dbm.Test.task_types,
                dbm.TestTaskType.task_type,
                dbm.TaskType.answer_forms,
            ),
            joinedload(
                dbm.Test.task_types,
                dbm.TestTaskType.task_type,
                dbm.TaskType.condition_forms,
            ),
            joinedload(
                dbm.Test.task_types, dbm.TestTaskType.task_type, dbm.TaskType.base_type
            ),
        )
        .where(dbm.Test.id == test_id, dbm.Test.user_id == user_id)
        .where(dbm.Test.deleted == False)
    )
    test: dbm.Test | None = await session.scalar(stmt)
    return test


async def get_test_by_link(session: AsyncSession, test_link: str) -> dbm.Test | None:
    stmt = (
        select(dbm.Test)
        .where(dbm.Test.link == test_link)
        .where(dbm.Test.deleted == False)
    )
    test: dbm.Test | None = await session.scalar(stmt)
    return test


async def create_test(
    session: AsyncSession, test_in: sch.TestCreate, **options
) -> dbm.Test:
    logger.debug(f"CRUD Test creation {test_in}...")

    # добавление теста
    db_test = make_new_test_data(test_in, **options)
    session.add(db_test)
    await session.flush()

    logger.debug(f"New test with id={db_test.id} added")

    # добавление типов заданий к тесту
    await add_task_type(session=session, ttys=test_in.task_types, test_id=db_test.id)

    # добавление вариантов к тесту
    await create_variant_for_test(
        session=session,
        test_id=db_test.id,
        variants_number=test_in.variants_number,
        task_types=test_in.task_types,
    )

    test = await get_test_by_id(
        session=session, test_id=db_test.id, user_id=options.get("user_id", 1)
    )
    return test


async def delete_test(
    session: AsyncSession,
    test: dbm.Test,
) -> None:
    setattr(test, "updated_at", datetime.now())
    setattr(test, "deleted", True)
    await session.commit()
