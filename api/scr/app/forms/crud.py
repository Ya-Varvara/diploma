"""

Read
"""

from typing import List

from sqlalchemy import select, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.forms.schemas import Form


async def get_all_forms(session: AsyncSession) -> List[Form]:
    stmt = select(dbm.Form)
    result: Result = await session.execute(stmt)
    forms = result.scalars().all()
    return list(forms)


async def create_condition_forms(
    session: AsyncSession, forms_ids: List[int], task_type_id: int
) -> None:
    for form_id in forms_ids:
        session.add(
            dbm.TaskTypesConditionForm(task_type_condition_form_id=task_type_id, form_id=form_id)
        )
    await session.commit()


async def create_answer_forms(
    session: AsyncSession, forms_ids: List[int], task_type_id: int
) -> None:
    for form_id in forms_ids:
        session.add(dbm.TaskTypesAnswerForm(task_type_answer_form_id=task_type_id, form_id=form_id))
    await session.commit()


async def update_condition_forms(
    session: AsyncSession, forms_ids: List[int], task_type_id: int
) -> None:
    await delete_old_condition_forms(session, task_type_id)
    await create_condition_forms(session, forms_ids, task_type_id)


async def update_answer_forms(
    session: AsyncSession, forms_ids: List[int], task_type_id: int
) -> None:
    await delete_old_answer_forms(session, task_type_id)
    await create_answer_forms(session, forms_ids, task_type_id)


async def delete_old_condition_forms(session: AsyncSession, task_type_id: int) -> None:
    await session.execute(
        delete(dbm.TaskTypesConditionForm).where(
            dbm.TaskTypesConditionForm.task_type_id == task_type_id
        )
    )
    await session.commit()


async def delete_old_answer_forms(session: AsyncSession, task_type_id: int) -> None:
    await session.execute(
        delete(dbm.TaskTypesAnswerForm).where(
            dbm.TaskTypesAnswerForm.task_type_id == task_type_id
        )
    )
    await session.commit()


async def add_condition_forms_to_task_type(
    forms_ids: List[int], task_type_id: int
) -> List[dbm.TaskTypesConditionForm]:
    return [
        dbm.TaskTypesConditionForm(task_type_id=task_type_id, form_id=form_id)
        for form_id in forms_ids
    ]


async def add_answer_forms_to_task_type(
    forms_ids: List[int], task_type_id: int
) -> List[dbm.TaskTypesAnswerForm]:
    return [
        dbm.TaskTypesAnswerForm(task_type_id=task_type_id, form_id=form_id)
        for form_id in forms_ids
    ]
