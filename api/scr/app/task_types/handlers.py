from typing import List

from api.scr.app.task_types import schemas as sch
from api.scr.app.forms import schemas as formsch
from api.scr.app.core import models as dbm


def make_full_task_type(task_types: List[dbm.TaskType]) -> List[sch.FullTaskType]:
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
