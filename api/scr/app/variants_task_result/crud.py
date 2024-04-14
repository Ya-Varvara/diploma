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
from api.scr.app.variants_task_result.handlers import make_new_variant_task_result_data


logger = logging.getLogger(__name__)


async def add_variant_task_result(
    session: AsyncSession, task_result_in: sch.VariantTaskResultCreate
) -> sch.VariantTaskResult:
    logger.debug(f"CRUD Adding variant task result... {task_result_in}")
    new = make_new_variant_task_result_data(res_in=task_result_in)
    session.add(new)
    await session.commit()
    return new
