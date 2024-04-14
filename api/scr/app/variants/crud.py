"""
Read
"""

import logging

from typing import List

from sqlalchemy import select, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.variants_task_result import schemas as sch


logger = logging.getLogger(__name__)


# async def add_variant(
#     session: AsyncSession, variant: sch.VariantTaskResultCreate
# ) -> sch.VariantTaskResult:
#     task_result_in.is_correct = await check_variant_task_result(
#         session=session, ttr=task_result_in
#     )
#     new = dbm.VariantsTaskResult(task_result_in.model_dump())
#     session.add(new)
#     session.flush()
#     return new
