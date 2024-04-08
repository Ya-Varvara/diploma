"""
Create
Read
Update
Delete
"""

from random import choice
from typing import Any, List
from datetime import datetime, timezone

from uuid import uuid4

from sqlalchemy import select, update
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, contains_eager
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.core.graph_generation.graph_gen import generate_graph

from api.scr.app.tests import schemas as sch

from api.scr.app.task_types import crud as task_type_crud
from api.scr.app.task_types.router import make_full_task_type

from api.scr.app.tasks import crud as task_crud


async def get_tests(session: AsyncSession, **options) -> list[dbm.Test]:
    print("CRUD GET TESTS")
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
    print(stmt)
    result: Result = await session.execute(stmt)
    tests = result.scalars().unique().all()
    return list(tests)


async def get_test_by_id(
    session: AsyncSession, test_id: int, user_id: int
) -> dbm.Test | None:
    stmt = (
        select(dbm.Test)
        .options(
            joinedload(dbm.Test.user),
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
    # print(stmt)
    test: dbm.Test | None = await session.scalar(stmt)
    return test


async def make_test_given(session: AsyncSession, test_id: int, variant: int) -> None:
    stmt = (
        update(dbm.TestTask)
        .where(dbm.TestTask.test_id == test_id)
        .where(dbm.TestTask.variant == variant)
        .values(is_given=True)
    )
    print(stmt)
    await session.execute(stmt)
    await session.commit()
    return


async def get_test_by_link_and_variant(
    session: AsyncSession, link: str, variant: int
) -> sch.TestVariant | None:
    print(variant)
    stmt = (
        select(dbm.Test)
        .join(dbm.TestTask)
        .options(contains_eager(dbm.Test.test_variants))
        .filter(dbm.TestTask.variant == variant)
        .where(dbm.Test.link == link)
    )
    print(stmt)
    test: dbm.Test | None = await session.scalar(stmt)
    tasks = []
    print(test.__dict__)
    for tt in test.test_variants:
        task = await task_crud.get_task_by_id(session, tt.task_id)
        print(task.__dict__)
        tfs = sch.TaskForStudent(
            name=task.name,
            type_id=task.type_id,
            description_data=task.description_data,
            condition_data=task.condition_data,
            type=make_full_task_type([task.type_name])[0],
        )
        tasks.append(tfs)

    result = sch.TestVariant(
        name=test.name,
        start_datetime=test.start_datetime,
        end_datetime=test.end_datetime,
        test_time=test.test_time,
        variant_number=variant,
        tasks=tasks,
        upload=test.upload,
    )
    await make_test_given(session, test.id, variant)
    return result


def make_new_test_data(test_in: sch.TestCreate, **options) -> dict[str, Any]:
    print("CRUD MAKE NEW TEST DATA")
    print(test_in)
    test_data = test_in.model_dump(
        exclude={"task_types", "start_datetime", "end_datetime", "test_time"}
    )

    test_data["start_datetime"] = test_in.start_datetime.replace(tzinfo=None)
    test_data["end_datetime"] = test_in.end_datetime.replace(tzinfo=None)
    test_data["test_time"] = test_in.test_time.replace(tzinfo=None)

    test_data["user_id"] = options.get("user_id", 1)
    test_data["link"] = str(uuid4())
    test_data["created_at"] = datetime.now()
    test_data["updated_at"] = datetime.now()
    test_data["deleted"] = False
    print(test_data)
    return test_data


async def add_task_types_to_test(
    session: AsyncSession, tasks: List[sch.TaskTypesForTestCreation], test_id: int
):
    for task in tasks:
        session.add(
            dbm.TestTaskType(
                test_id=test_id, task_type_id=task.type_id, number=task.number
            )
        )
    await session.commit()
    return


async def get_task_for_test(
    session: AsyncSession,
    task_type: dbm.TaskType,
    user_id: int,
) -> dbm.Task:
    print("CRUD GET TASK FOR TEST")
    if task_type.base_task_type == 1:
        print("CRUD GET TASK FOR TEST GRAPH")
        graph_data = await generate_graph(**task_type.settings)
        task = dbm.Task(
            name=f"graph_{uuid4()}",
            type_id=task_type.id,
            description_data=graph_data.get("description_data", ""),
            condition_data=graph_data.get("condition_data", {}),
            answer_data=graph_data.get("answer_data", {}),
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            deleted=False,
        )
        session.add(task)
        await session.flush()
        print(task.__dict__)
        return task
    else:
        print("CRUD GET TASK FOR TEST BASE")
        stmt = (
            select(dbm.Task)
            .where(dbm.Task.type_id == task_type.id)
            .where(dbm.Task.deleted == False)
            .where(dbm.Task.user_id == user_id)
        )
        result: Result = await session.execute(stmt)
        task = result.scalar()
        return task


async def add_test_task_for_variants(
    session: AsyncSession,
    test_id: int,
    task_type: dbm.TaskType,
    tasks_num: int,
    variants: int,
    user_id: int,
):
    print("CRUD ADD TEST TASK FOR VARIANTS")
    for i in range(variants):
        task_ids = set()
        print(i)
        for _ in range(tasks_num):
            task = await get_task_for_test(session, task_type, user_id)
            print(task.__dict__)
            # while task.id in task_ids:
            #     task = await get_task_for_test(session, task_type, user_id)

            task_ids.add(task.id)
            session.add(
                dbm.TestTask(
                    variant=i + 1, test_id=test_id, task_id=task.id, is_given=False
                )
            )
    await session.commit()


async def create_test(
    session: AsyncSession, test_in: sch.TestCreate, **options
) -> dbm.Test:
    print("CRUD CREATE TEST")
    test_data = make_new_test_data(test_in, **options)
    test = dbm.Test(**test_data)
    session.add(test)
    await session.flush()
    print("TEST ID", test.id)
    print("CRUD ADD TASK TYPES")
    await add_task_types_to_test(session, test_in.task_types, test.id)

    result = await session.execute(
        select(dbm.Test)
        .where(dbm.Test.id == test.id)
        .options(
            joinedload(dbm.Test.task_types),
            joinedload(dbm.Test.task_types, dbm.TestTaskType.task_type),
        )
    )
    test = result.scalars().first()
    print(test.__dict__)

    print("CRUD ADD TASKS")
    for task_type in test.task_types:
        print(task_type.__dict__)
        await add_test_task_for_variants(
            session=session,
            test_id=test.id,
            task_type=task_type.task_type,
            tasks_num=task_type.number,
            variants=test.variants_number,
            user_id=test.user_id,
        )
    await session.flush()
    return test


async def get_free_variant_number(session: AsyncSession, link: str) -> int | None:
    stmt = (
        select(dbm.TestTask.variant)
        .join(dbm.Test, dbm.Test.id == dbm.TestTask.test_id)
        .where(
            dbm.Test.link == link,
            dbm.TestTask.is_given == False,
            dbm.Test.deleted == False,
        )
        .distinct()
    )

    result: Result = await session.execute(stmt)
    variants = list(result.scalars().unique().all())

    if variants:
        return choice(variants)

    return None


# async def update_test(
#     session: AsyncSession,
#     test: Test,
#     test_update: TestUpdate | TestUpdatePartial,
#     partial: bool = False,
# ) -> Test:
#     for name, value in test_update.model_dump(exclude_unset=partial).items():
#         setattr(test, name, value)
#     await session.commit()
#     return test


async def delete_test(
    session: AsyncSession,
    test: dbm.Test,
) -> None:
    setattr(test, "updated_at", datetime.now())
    setattr(test, "deleted", True)
    await session.commit()
