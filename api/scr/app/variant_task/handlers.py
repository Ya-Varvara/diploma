import logging
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.variant_task import schemas as sch
from api.scr.app.tests.schemas import TaskTypesForTestCreation

from api.scr.app.task_types.crud import get_task_type_by_id
from api.scr.app.tasks.handlers import get_task_for_test
from api.scr.app.tasks.handlers import make_full_tasks
from api.scr.app.variants_task_result.handlers import make_variant_task_result


logger = logging.getLogger(__name__)


async def add_tasks_to_variants(
    session: AsyncSession,
    variant_ids: List[int],
    task_types: List[TaskTypesForTestCreation],
    **options,
):
    for tt in task_types:
        type_id = tt.type_id
        number = tt.number

        task_type = await get_task_type_by_id(session, type_id, **options)
        if task_type is None:
            logger.error(f"Task type with id={type_id} was not found")
            continue

        for variant_id in variant_ids:
            task_ids = set()
            for _ in range(number):
                task = await get_task_for_test(session, task_type, **options)

                if task is None:
                    logger.error(f"Task with type {task_type.name} was not found")
                    continue

                while task.id in task_ids:
                    task = await get_task_for_test(session, task_type, **options)
                task_ids.add(task.id)

                session.add(dbm.VariantTask(variant_id=variant_id, task_id=task.id))
    await session.commit()
    return


def make_variant_tasks_for_teacher(
    vts: List[dbm.VariantTask],
) -> List[sch.VariantTaskForTeacher]:
    logger.debug(f"HANDLERS Making variant tasks for teacher...")
    result = []
    for vartask in vts:
        new = sch.VariantTaskForTeacher(
            variant_id=vartask.variant_id,
            task_id=vartask.task_id,
            id=vartask.id,
            task=make_full_tasks([vartask.task])[0],
            students_result=make_variant_task_result([vartask.task_result])[0],
        )
        result.append(new)
    return result
