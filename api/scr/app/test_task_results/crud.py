"""
Create
Read
Update
Delete
"""

from typing import Any, List

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.test_task_results import schemas as sch

from api.scr.app.tasks import crud as tasks_crud
from api.scr.app.test_tasks import crud as test_tasks_crud

from api.scr.app.task_types.router import make_full_task_type


async def make_full_test_task_result_data(tt: dbm.TestTask):
    print(tt.__dict__)
    new = sch.FullTestTaskResult(
        id=tt.result.id,
        test_task_id=tt.id,
        answer=sch.AnswerData(
            type=tt.result.answer["type"], data=tt.result.answer["data"]
        ),
        students_info=sch.StudentsData(
            name=tt.result.students_info["name"],
            surname=tt.result.students_info["surname"],
        ),
        time_data=sch.TimeData(
            start_time=tt.result.start_datetime, end_time=tt.result.end_datetime
        ),
        is_correct=tt.result.is_correct,
        task=sch.FullTask(
            name=tt.task.name,
            type_id=tt.task.type_id,
            description_data=tt.task.description_data,
            condition_data=tt.task.condition_data,
            answer_data=tt.task.answer_data,
            id=tt.task.id,
            created_at=tt.task.created_at,
            updated_at=tt.task.updated_at,
            deleted=tt.task.deleted,
            type=make_full_task_type([tt.task.type_name])[0],
        ),
    )
    return new


async def get_test_task_results(
    session: AsyncSession,
    test_id: int,
    variant: int,
) -> List[sch.FullTestTaskResult] | None:
    stmt = (
        select(dbm.TestTask)
        .options(
            joinedload(dbm.TestTask.task),
            joinedload(dbm.TestTask.uploaded_file),
            joinedload(dbm.TestTask.task, dbm.Task.type_name),
            joinedload(
                dbm.TestTask.task, dbm.Task.type_name, dbm.TaskType.answer_forms
            ),
            joinedload(
                dbm.TestTask.task, dbm.Task.type_name, dbm.TaskType.condition_forms
            ),
            joinedload(dbm.TestTask.result),
        )
        .where(dbm.TestTask.test_id == test_id, dbm.TestTask.variant == variant)
    )
    print(stmt)
    result: Result = await session.execute(stmt)
    test_tasks = result.scalars().unique().all()
    print(test_tasks)
    res = [await make_full_test_task_result_data(tt=tt) for tt in test_tasks]
    return res


async def check_test_task_result(
    session: AsyncSession, ttr: sch.TestTaskResultCreate
) -> bool | None:
    test_task = await test_tasks_crud.get_test_task_by_id(
        session=session, test_task_id=ttr.test_task_id
    )
    task = await tasks_crud.get_task_by_id(session=session, task_id=test_task.task_id)
    if task.type_name.base_type.id == 1:
        correct_answer = task.answer_data["max_flow"]
        if correct_answer == int(ttr.answer.data):
            return True
    return False


async def make_test_task_result_data(
    session: AsyncSession, ttr: sch.TestTaskResultCreate
) -> dict[str, Any]:
    newttr = ttr.model_dump(exclude={"time_data"})
    newttr["start_datetime"] = ttr.time_data.start_time.replace(tzinfo=None)
    newttr["end_datetime"] = ttr.time_data.end_time.replace(tzinfo=None)
    newttr["is_correct"] = await check_test_task_result(session=session, ttr=ttr)
    return newttr


async def create_test_task_results(
    session: AsyncSession, test_task_results_in: List[sch.TestTaskResultCreate]
) -> None:
    for ttr in test_task_results_in:
        test_task_data = await make_test_task_result_data(session=session, ttr=ttr)
        test_task_result = dbm.TestTaskResult(**test_task_data)
        session.add(test_task_result)
    await session.commit()
    return
