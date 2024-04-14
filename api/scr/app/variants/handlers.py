import logging
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.variants import schemas as sch
from api.scr.app.tests.schemas import TaskTypesForTestCreation

from api.scr.app.variant_task.handlers import add_tasks_to_variants
from api.scr.app.tests.handlers import make_test_data_for_variant
from api.scr.app.variant_result_info.handlers import make_variant_result_info
from api.scr.app.uploaded_files.handlers import make_uploaded_files_info
from api.scr.app.tasks.handlers import make_tasks_for_student
from api.scr.app.variant_task.handlers import (
    make_variant_tasks_for_teacher,
    make_variant_tasks_for_student,
)


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


def make_variant_for_teacher(
    variants: List[dbm.Variant],
) -> List[sch.VariantForTeacher]:
    logger.debug(f"HANDLERS Making variant for teacher...")
    result = []
    for var in variants:
        vri = make_variant_result_info([var.result_info])
        uf = make_uploaded_files_info([var.uploaded_file])
        new = sch.VariantForTeacher(
            id=var.id,
            variant=var.variant,
            test_info=make_test_data_for_variant([var.test])[0],
            variant_result_info=None if not vri else vri[0],
            uploaded_file=None if not uf else uf[0],
            is_given=var.is_given,
            tasks=make_variant_tasks_for_teacher(var.tasks),
        )
        result.append(new)
    return result


def make_variant_for_student(
    variants: List[dbm.Variant],
) -> List[sch.VariantForStudent]:
    logger.debug(f"HANDLERS Making variant for student...")
    result = []
    for var in variants:
        new = sch.VariantForStudent(
            id=var.id,
            variant=var.variant,
            test_info=make_test_data_for_variant([var.test])[0],
            tasks=make_variant_tasks_for_student(var.tasks),
        )
        result.append(new)
    return result
