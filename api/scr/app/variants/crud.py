"""
Read
"""

import logging

from typing import List

from sqlalchemy import select, delete
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.variants_task_result import schemas as sch


logger = logging.getLogger(__name__)


async def get_all_variants_for_test(
    session: AsyncSession, test_id: int, **options
) -> List[dbm.Variant]:
    stmt = (
        select(dbm.Variant)
        .options(
            joinedload(dbm.Variant.test),
            joinedload(dbm.Variant.uploaded_file),
            joinedload(dbm.Variant.result_info),
            joinedload(dbm.Variant.tasks),
            joinedload(dbm.Variant.tasks, dbm.VariantTask.task_result),
            joinedload(dbm.Variant.tasks, dbm.VariantTask.task),
            joinedload(dbm.Variant.tasks, dbm.VariantTask.task, dbm.Task.type),
            joinedload(
                dbm.Variant.tasks,
                dbm.VariantTask.task,
                dbm.Task.type,
                dbm.TaskType.answer_forms,
            ),
            joinedload(
                dbm.Variant.tasks,
                dbm.VariantTask.task,
                dbm.Task.type,
                dbm.TaskType.condition_forms,
            ),
        )
        .where(dbm.Variant.test_id == test_id)
        .order_by(dbm.Variant.is_given, dbm.Variant.variant)
    )
    result: Result = await session.execute(stmt)
    variants = result.scalars().unique().all()
    return list(variants)


async def get_variant_for_test(
    session: AsyncSession, test_id: int, **options
) -> dbm.Variant:
    stmt = (
        select(dbm.Variant)
        .options(
            joinedload(dbm.Variant.test),
            joinedload(dbm.Variant.tasks),
            joinedload(dbm.Variant.tasks, dbm.VariantTask.task),
            joinedload(dbm.Variant.tasks, dbm.VariantTask.task, dbm.Task.type),
            joinedload(
                dbm.Variant.tasks,
                dbm.VariantTask.task,
                dbm.Task.type,
                dbm.TaskType.answer_forms,
            ),
            joinedload(
                dbm.Variant.tasks,
                dbm.VariantTask.task,
                dbm.Task.type,
                dbm.TaskType.condition_forms,
            ),
        )
        .where(dbm.Variant.test_id == test_id)
        .where(dbm.Variant.is_given == False)
    )
    result: Result = await session.execute(stmt)
    variant = result.first()
    if variant is not None:
        return variant[0]
    return None


async def make_test_variant_given(
    session: AsyncSession, test_variant_id: int, **options
) -> dbm.Variant:
    stmt = select(dbm.Variant).where(dbm.Variant.id == test_variant_id)
    result: Result = await session.execute(stmt)
    variant = result.first()[0]
    setattr(variant, "is_given", True)
    await session.commit()
    return variant
