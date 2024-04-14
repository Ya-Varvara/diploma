import logging
from typing import List
from datetime import datetime

from api.scr.app.task_types import schemas as sch
from api.scr.app.forms import schemas as formsch
from api.scr.app.core import models as dbm
from api.scr.app.task_types.schemas import TaskTypeCreate


logger = logging.getLogger(__name__)


def make_full_task_type(task_types: List[dbm.TaskType]) -> List[sch.FullTaskType]:
    logger.debug(f"HANDLERS Making full task type...")
    result = []
    for tt in task_types:
        newtt = sch.FullTaskType(
            id=tt.id,
            name=tt.name,
            created_at=tt.created_at,
            updated_at=tt.updated_at,
            answer_forms=[formsch.Form.from_orm(af) for af in tt.answer_forms],
            condition_forms=[formsch.Form.from_orm(cf) for cf in tt.condition_forms],
            settings=tt.settings,
            base_task_type=tt.base_task_type,
            user_id=tt.user_id,
            deleted=tt.deleted,
        )
        result.append(newtt)
    return result


def make_new_task_type_data(tt: TaskTypeCreate, user_id: int) -> dbm.TaskType:
    task_type = dbm.TaskType(
        **tt.model_dump(exclude={"condition_forms", "answer_forms"})
    )
    task_type.user_id = user_id
    task_type.created_at = datetime.now()
    task_type.updated_at = datetime.now()
    task_type.deleted = False
    return task_type
