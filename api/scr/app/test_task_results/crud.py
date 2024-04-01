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
from api.scr.app.core.models import TestTaskResult


# async def get_test_task_results(session: AsyncSession) -> list[TestTaskResult]:
#     stmt = select(TestTaskResult).order_by(TestTaskResult.id)
#     result: Result = await session.execute(stmt)
#     test_task_results = result.scalars().all()
#     return list(test_task_results)


# async def get_test_task_result(
#     session: AsyncSession, test_task_result_id: int
# ) -> TestTaskResult | None:
#     return await session.get(TestTaskResult, test_task_result_id)


# async def create_test_task_result(
#     session: AsyncSession, test_task_result_in: TestTaskResultCreate
# ) -> TestTaskResult:
#     test_task_result = TestTaskResult(**test_task_result_in.model_dump())
#     session.add(test_task_result)
#     await session.commit()
#     # await session.refresh(product)
#     return test_task_result


# async def update_test_task_result(
#     session: AsyncSession,
#     test_task_result: TestTaskResult,
#     test_task_result_update: TestTaskResultUpdate | TestTaskResultUpdatePartial,
#     partial: bool = False,
# ) -> TestTaskResult:
#     for name, value in test_task_result_update.model_dump(
#         exclude_unset=partial
#     ).items():
#         setattr(test_task_result, name, value)
#     await session.commit()
#     return test_task_result


# async def delete_test_task_result(
#     session: AsyncSession,
#     test_task_result: TestTaskResult,
# ) -> None:
#     await session.delete(test_task_result)
#     await session.commit()
