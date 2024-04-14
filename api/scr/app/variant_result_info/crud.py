"""
Read
"""

from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.variant_result_info import schemas as sch


async def add_variant_result_info(
    session: AsyncSession, info_in: sch.VariantResultInfoCreate
) -> sch.VariantResultInfo:
    new = dbm.VariantResultInfo(info_in.model_dump())
    session.add(new)
    await session.flush()
    return new
