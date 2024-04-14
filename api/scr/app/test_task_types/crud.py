"""
Add
"""

import logging
from typing import List

from sqlalchemy import select, update
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, contains_eager
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm

from api.scr.app.tests import schemas as sch


logger = logging.getLogger(__name__)


async def add_task_type(
    session: AsyncSession, ttys: List[sch.TaskTypesForTestCreation], test_id: int
) -> None:

    logger.debug(f"Add task types {len(ttys)} for test with id={test_id}")
    for tty in ttys:
        session.add(
            dbm.TestTaskType(
                test_id=test_id, task_type_id=tty.type_id, number=tty.number
            )
        )
    await session.commit()
    return
