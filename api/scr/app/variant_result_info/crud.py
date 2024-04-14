"""
Read
"""

import logging
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.variant_result_info import schemas as sch
from api.scr.app.variant_result_info.handlers import make_new_variant_result_info


logger = logging.getLogger(__name__)


async def add_variant_result_info(
    session: AsyncSession, info_in: sch.VariantResultInfoCreate
) -> sch.VariantResultInfo:
    logger.debug(f"CRUD Adding variant result info...")
    new = make_new_variant_result_info(info_in)
    session.add(new)
    await session.commit()
    return new
