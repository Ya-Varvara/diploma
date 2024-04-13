"""
Read
"""

from typing import List

from sqlalchemy import select, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.variants_task_result import schemas as sch


async def add_variant_task_result(
    session: AsyncSession, task_result_in: sch.VariantTaskResultCreate
) -> sch.VariantTaskResult:
    task_result_in.is_correct = await check_variant_task_result(session=session, ttr=task_result_in)
    new = dbm.VariantsTaskResult(task_result_in.model_dump())
    session.add(new)
    session.flush()
    return new


async def check_variant_task_result(
    session: AsyncSession, ttr: sch.VariantTaskResultCreate
) -> bool | None:
    # task = await test_tasks_crud.get_test_task_by_id(
    #     session=session, test_task_id=ttr.test_task_id
    # )
    # task = await tasks_crud.get_task_by_id(session=session, task_id=test_task.task_id)
    # if task.type.base_type.id == 1:
    #     correct_answer = task.answer_data["max_flow"]
    #     if correct_answer == int(ttr.answer.data):
    #         return True
    return False
