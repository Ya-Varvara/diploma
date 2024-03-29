from typing import List
from json import loads
from datetime import datetime, time
from random import randint

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.database import get_async_session

from api.scr.app.core import models as dbm

from api.scr.app.core.graph_generation.graph_gen import generate_graph

from api.scr.app.tests import crud
from api.scr.app.tests import schemas as sch
from api.scr.app.tests import dependences as deps

from api.scr.app.task_types.crud import get_task_type_by_name
from api.scr.app.task_types.router import make_full_task_type

from api.scr.app.tasks import crud as task_crud
from api.scr.app.tasks import schemas as task_sch

from api.scr.app.test_tasks import crud as test_task_crud
from api.scr.app.test_tasks import schemas as test_task_sch

from api.scr.app.auth.router import get_current_user


router = APIRouter(prefix="/test", tags=["Test"])


def make_full_test(tests: List[dbm.Test]) -> List[sch.Test]:
    result = []
    for test in tests:
        newtest = sch.FullTest(
            name=test.name,
            start_datetime=test.start_datetime,
            end_datetime=test.end_datetime,
            test_time=test.test_time,
            variants_number=test.variants_number,
            id=test.id,
            user_id=test.user_id,
            link=test.link,
            created_at=test.created_at,
            updated_at=test.updated_at,
            deleted=test.deleted,
            task_types=[
                sch.TaskTypesForFullTest(
                    type=make_full_task_type([t.task_type])[0], number=t.number
                )
                for t in test.task_types
            ],
        )
        result.append(newtest)
    return result


def make_test_for_student(test: dbm.Test) -> sch.TestVariant:
    newtest = sch.FullTest(
        name=test.name,
        start_datetime=test.start_datetime,
        end_datetime=test.end_datetime,
        test_time=test.test_time,
        variants_number=test.variants_number,
        id=test.id,
        user_id=test.user_id,
        link=test.link,
        created_at=test.created_at,
        updated_at=test.updated_at,
        deleted=test.deleted,
        task_types=[
            sch.TaskTypesForFullTest(
                type=make_full_task_type([t.task_type])[0], number=t.number
            )
            for t in test.task_types
        ],
    )
    return newtest


@router.get("/", response_model=list[sch.FullTest])
async def get_tests(
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
):
    print("ROUTER GET TESTS")
    options = {"user_id": user.id}
    tests = await crud.get_tests(session=session, options=options)
    return make_full_test(tests)


@router.post(
    "/",
    response_model=sch.FullTest,
    status_code=status.HTTP_201_CREATED,
)
async def create_test(
    test_in: sch.TestCreate,
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
):
    print("ROUTER CREATE TEST")
    options = {"user_id": user.id}
    test = await crud.create_test(session=session, test_in=test_in, **options)
    return make_full_test([test])[0]


@router.get(
    "/{test_id}/",
    response_model=sch.FullTest,
)
async def get_test(
    test_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
):
    test = await crud.get_test_by_id(session=session, test_id=test_id, user_id=user.id)
    if test is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Test not found"
        )
    return make_full_test([test])[0]


# # @router.put("/{test_id}/")
# async def update_test(
#     test_update: TestUpdate,
#     test: Test = Depends(test_by_id),
#     session: AsyncSession = Depends(get_async_session),
#     user: User = Depends(get_current_user()),
# ):
#     return await crud.update_test(session=session, test=test, test_update=test_update)


# # @router.patch("/{test_id}/")
# async def update_test_partial(
#     test_update: TestUpdatePartial,
#     test: Test = Depends(test_by_id),
#     session: AsyncSession = Depends(get_async_session),
# ):
#     return await crud.update_test(
#         session=session,
#         test=test,
#         test_update=test_update,
#         partial=True,
#     )


@router.delete("/{test_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test(
    test_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
) -> None:
    test = await crud.get_test_by_id(session=session, test_id=test_id, user_id=user.id)
    if test is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Test not found"
        )
    await crud.delete_test(session=session, test=test)


@router.get(
    "/variant/{test_link}",
    status_code=status.HTTP_200_OK,
    response_model=sch.TestVariant,
)
async def get_variant(link: str, session: AsyncSession = Depends(get_async_session)):
    # test = await crud.get_test_by_link(session=session, link="test")
    variant = await crud.get_free_variant_number(session=session, link=link)

    if variant is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Test not found"
        )

    return await crud.get_test_by_link_and_variant(
        session=session, link=link, variant=variant
    )
