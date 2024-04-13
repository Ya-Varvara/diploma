"""
Read
"""

from typing import List

from sqlalchemy import select, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.variant_task import schemas as sch


async def add_variant_task(
    session: AsyncSession, task_in: sch.VariantTaskCreate
) -> sch.VariantTaskResult:
    new = dbm.VariantTask(task_in.model_dump())
    session.add(new)
    session.flush()
    return new
