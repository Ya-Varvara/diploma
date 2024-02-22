from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.database import get_async_session

from api.scr.app.core.models import Test
from api.scr.app.tests.schemas import TestVariant
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload

import api.scr.app.tests.crud as crud


async def test_by_id(
    test_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> Test:
    test = await crud.get_test(session=session, test_id=test_id)
    if test is not None:
        return test

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {test_id} not found!",
    )


async def test_by_link(
    test_link: str,
    session: AsyncSession = Depends(get_async_session),
) -> Test:
    stmt = (
        select(Test)
        .options(joinedload(Test.test_variants))
        .where(Test.link == test_link)
    )
    result: Result = await session.execute(statement=stmt)
    test: Test = result.scalar()
    return test
