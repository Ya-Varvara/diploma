from typing import List
from json import loads
from datetime import datetime, time
from random import randint

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession


from scr.app.database import get_async_session
from scr.app.core.models import TaskType, Task, User, Test as TestModel, TestTask

from scr.app.core.graph_generation.graph_gen import generate_graph


import scr.app.tests.crud as crud
from scr.app.tests.schemas import (
    TestCreate,
    TestUpdate,
    TestUpdatePartial,
    Test,
    TestOut,
    DescriptionBase,
    TestVariant,
)
from scr.app.tests.dependences import test_by_id, test_by_link

from scr.app.task_types.crud import get_task_type_by_name, get_task_type

from scr.app.tasks.crud import get_task_by_name, create_task, get_task
from scr.app.tasks.schemas import TaskCreate, TaskBase

from scr.app.test_tasks.crud import create_test_task, update_test_task
from scr.app.test_tasks.schemas import TestTaskCreate, TestTaskUpdatePartial

from scr.app.auth.router import get_current_user


router = APIRouter(prefix="/test", tags=["Test"])


def create_test_model(test) -> Test:
    return Test(
        id=test.id,
        name=test.name,
        user_id=test.user_id,
        link=test.link,
        description=DescriptionBase(
            students_number=test.description["students_number"],
            description=test.description["description"],
            tasks=test.description["tasks"],
            deadline=datetime.fromisoformat(test.description["deadline"]),
            time=time.fromisoformat(test.description["time"]),
        ),
    )


@router.get("/", response_model=list[Test])
async def get_tests(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user()),
):
    options = {"user_id": user.id}
    return await crud.get_tests(session=session, options=options)


@router.post(
    "/",
    response_model=Test,
    status_code=status.HTTP_201_CREATED,
)
async def create_test(
    test_in: TestCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user()),
):
    options = {"user_id": user.id}
    test = await crud.create_test(
        session=session,
        test_in=crud.make_new_test_data(test_in=test_in, options=options),
    )

    raw_task_types = test_in.description.tasks
    task_types_list = {}
    for key, value in raw_task_types.items():
        task_type: TaskType = await get_task_type_by_name(
            session=session, task_type_name=key
        )
        if task_type is None:
            continue
        task_types_list[task_type.id] = value

    for var in range(test_in.description.students_number):
        for task_type_id, num in task_types_list.items():
            task_type: TaskType = await get_task_type(
                session=session, task_type_id=task_type_id
            )
            task_ids = []
            for _ in range(num):
                task: Task
                if task_type.name == "graph":
                    data = generate_graph()
                    task = await create_task(
                        session=session,
                        task_in=TaskCreate(
                            name="some_name",
                            type_id=task_type.id,
                            data=data,
                        ),
                        user_id=user.id,
                    )
                else:
                    i = randint(0, len(task_type.tasks) - 1)
                    while i in task_ids:
                        i = randint(0, len(task_type.tasks) - 1)
                    task_ids.append(i)
                    task = task_type.tasks[i]
                test_task = await create_test_task(
                    session=session,
                    test_task_in=TestTaskCreate(
                        variant=var + 1, test_id=test.id, task_id=task.id
                    ),
                )
    return test


@router.get(
    "/{test_id}/",
    response_model=Test,
)
async def get_test(
    test_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user()),
):
    test = await crud.get_test(session=session, test_id=test_id, user_id=user.id)
    if test is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Test not found"
        )
    return test


# @router.put("/{test_id}/")
async def update_test(
    test_update: TestUpdate,
    test: Test = Depends(test_by_id),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user()),
):
    return await crud.update_test(session=session, test=test, test_update=test_update)


# @router.patch("/{test_id}/")
async def update_test_partial(
    test_update: TestUpdatePartial,
    test: Test = Depends(test_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.update_test(
        session=session,
        test=test,
        test_update=test_update,
        partial=True,
    )


@router.delete("/{test_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test(
    test_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user()),
) -> None:
    test = await crud.get_test(session=session, test_id=test_id, user_id=user.id)
    if test is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Test not found"
        )
    await crud.delete_test(session=session, test=test)


@router.get(
    "/variant/{test_link}", status_code=status.HTTP_200_OK, response_model=TestVariant
)
async def get_variant(
    session: AsyncSession = Depends(get_async_session),
    test: TestModel = Depends(test_by_link),
) -> TestVariant:
    variant: int = None
    test_tasks: List[TestTask] = []
    tasks: List[Task] = []

    for test_task in test.test_variants:
        if test_task.is_given:
            continue
        if variant is None:
            variant = test_task.variant
        if test_task.variant == variant:
            test_tasks.append(test_task)
            await update_test_task(
                session=session,
                test_task=test_task,
                test_task_update=TestTaskUpdatePartial(is_given=True),
                partial=True,
            )
            task: Task = await get_task(session=session, task_id=test_task.task_id)
            print(type(task))
            tasks.append(task)

    if not test_tasks:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="All variants are given",
        )

    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There are no tasks in test",
        )

    test_variant = TestVariant(
        name=test.name,
        variant_number=variant,
        description=test.description["description"],
        tasks=[],
    )
    for t in tasks:
        print(type(t))
        students_data = t.data.get("students_data", {})
        test_variant.tasks.append(
            TaskBase(name=t.name, type_id=t.type_id, data=students_data)
        )
    return test_variant
