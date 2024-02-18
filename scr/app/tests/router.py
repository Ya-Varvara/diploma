from typing import List
from json import loads
from datetime import datetime, time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from scr.app.database import get_async_session
from scr.app.tests.schemas import (
    TestCreate,
    TestUpdate,
    TestUpdatePartial,
    Test,
    TestOut,
    DescriptionBase,
)
from scr.app.tests.dependences import test_by_id

import scr.app.tests.crud as crud

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
async def get_tests(session: AsyncSession = Depends(get_async_session)):
    return await crud.get_tests(session=session)


@router.post(
    "/",
    response_model=Test,
    status_code=status.HTTP_201_CREATED,
)
async def create_test(
    test_in: TestCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.create_test(session=session, test_in=test_in)


@router.get("/{test_id}/", response_model=Test)
async def get_test(test: Test = Depends(test_by_id)):
    return test


@router.put("/{test_id}/")
async def update_test(
    test_update: TestUpdate,
    test: Test = Depends(test_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.update_test(session=session, test=test, test_update=test_update)


@router.patch("/{test_id}/")
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
    test: Test = Depends(test_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await crud.delete_test(session=session, test=test)
