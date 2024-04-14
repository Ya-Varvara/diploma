import logging
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.tests.schemas import TaskTypesForTestCreation

from api.scr.app.variant_task.handlers import add_tasks_to_variants


logger = logging.getLogger(__name__)


async def create_variant_for_test(
    session: AsyncSession,
    test_id: int,
    variants_number: int,  # количество вариантов
    task_types: List[TaskTypesForTestCreation],
    **options,
):
    # добавление тестов
    variant_ids: List[int] = []
    for i in range(1, variants_number + 1):
        variant = dbm.Variant(variant=i, test_id=test_id, is_given=False)
        session.add(variant)
        await session.flush()
        logger.debug(f"Add variant with id={variant.id}")
        variant_ids.append(variant.id)

    logger.debug(f"Added to test id={test_id} variants with ids={variant_ids}")

    # добавление заданий к тестам
    await add_tasks_to_variants(session, variant_ids, task_types, **options)
