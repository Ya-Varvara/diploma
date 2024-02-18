"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from scr.app.core.models import Test

from scr.app.tests.schemas import TestCreate, TestUpdate, TestUpdatePartial


async def get_tests(session: AsyncSession) -> list[Test]:
    stmt = select(Test).options(joinedload(Test.user)).order_by(Test.id)
    result: Result = await session.execute(stmt)
    tests = result.scalars().all()
    return list(tests)


async def get_test(session: AsyncSession, test_id: int) -> Test | None:
    return await session.get(Test, test_id)


async def create_test(session: AsyncSession, test_in: TestCreate) -> Test:
    dict_test_in = test_in.model_dump(exclude={"description"})
    print(dict_test_in)
    dict_test_in["description"] = test_in.description.model_dump()
    dict_test_in["description"]["time"] = str(test_in.description.time)
    dict_test_in["description"]["deadline"] = str(test_in.description.deadline)
    print(dict_test_in)

    test = Test(**dict_test_in)

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