from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from scr.app.database import get_async_session

from scr.app.core.models import Test

import scr.app.tests.crud as crud


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
