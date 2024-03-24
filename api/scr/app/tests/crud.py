"""
Create
Read
Update
Delete
"""

from typing import Any

from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from api.scr.app.core.models import Test

from api.scr.app.tests.schemas import TestCreate, TestUpdate, TestUpdatePartial


async def get_tests(session: AsyncSession, **options) -> list[Test]:
    stmt = select(Test).options(joinedload(Test.user)).order_by(Test.id)
    if user_id := options.get("user_id", ""):
        stmt = stmt.where(Test.user_id == user_id)
    result: Result = await session.execute(stmt)
    tests = result.scalars().all()
    return list(tests)


async def get_test(session: AsyncSession, test_id: int, user_id: int) -> Test | None:
    stmt = (
        select(Test)
        .options(joinedload(Test.user))
        .where(Test.id == test_id, Test.user_id == user_id)
    )
    # print(stmt)
    result: Result = await session.execute(stmt)
    test = result.scalar()
    return test


def make_new_test_data(test_in: TestCreate, **options) -> dict[str, Any]:
    test_data = test_in.model_dump(exclude={"description"})

    test_data["description"] = test_in.description.model_dump()
    test_data["description"]["time"] = str(test_in.description.time)
    test_data["description"]["deadline"] = str(test_in.description.deadline)

    test_data["user_id"] = options.get("user_id", 1)
    test_data["link"] = str(uuid4())

    return test_data


async def create_test(session: AsyncSession, test_in: dict[str, Any]) -> Test:
    test = Test(**test_in)
    session.add(test)
    await session.commit()
    return test


async def update_test(
    session: AsyncSession,
    test: Test,
    test_update: TestUpdate | TestUpdatePartial,
    partial: bool = False,
) -> Test:
    for name, value in test_update.model_dump(exclude_unset=partial).items():
        setattr(test, name, value)
    await session.commit()
    return test


async def delete_test(
    session: AsyncSession,
    test: Test,
) -> None:
    await session.delete(test)
    await session.commit()
