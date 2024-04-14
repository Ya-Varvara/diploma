import logging
from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm
from api.scr.app.core.graph_generation.graph_gen import generate_graph


logger = logging.getLogger(__name__)


async def get_task_for_test(
    session: AsyncSession,
    task_type: dbm.TaskType,
    **options,
) -> dbm.Task | None:
    logger.debug(f"HANDLERS Getting task for test variant...")
    user_id = options.get("user_id", 1)

    if task_type.base_task_type == 1:
        graph_data = await generate_graph(**task_type.settings)
        task = dbm.Task(
            name=f"graph_{uuid4()}",
            type_id=task_type.id,
            description_data=graph_data.get("description_data", ""),
            condition_data=graph_data.get("condition_data", {}),
            answer_data=graph_data.get("answer_data", {}),
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            deleted=False,
        )
        session.add(task)
        await session.flush()
        logger.debug(f"HANDLERS Task with type {task_type.name} created {task.id}")
        return task
    else:
        stmt = (
            select(dbm.Task)
            .where(dbm.Task.type_id == task_type.id)
            .where(dbm.Task.deleted == False)
            .where(dbm.Task.user_id == user_id)
        )
        result: Result = await session.execute(stmt)
        task: dbm.Task | None = result.scalar()
        logger.debug(f"HANDLERS Task with type {task_type.name} found {task.id}")
        return task
