import logging
from typing import List
from api.scr.app.core import models as dbm
from api.scr.app.variants_task_result import schemas as sch


logger = logging.getLogger(__name__)


def make_variant_task_result(
    vris: List[dbm.VariantsTaskResult],
) -> List[sch.VariantTaskResult]:
    logger.debug(f"HANDLERS Making variant task result... {vris}")
    result = []
    for vr in vris:
        if vr is None:
            continue
        result.append(sch.VariantTaskResult.model_validate(vr))
    print(result)
    return result

def make_new_variant_task_result_data(res_in: sch.VariantTaskResultCreate, **options) -> dbm.VariantsTaskResult:
    logger.debug(f"HANDLERS Making new variant task result data...")
    data = res_in.model_dump()

    data["is_correct"] = check_variant_task_result(ttr=res_in)

    logger.debug(f"HANDLERS New variant task result data {data}")

    return dbm.VariantsTaskResult(**data)

def check_variant_task_result(
    ttr: sch.VariantTaskResultCreate
) -> bool | None:
    # task = await test_tasks_crud.get_test_task_by_id(
    #     session=session, test_task_id=ttr.test_task_id
    # )
    # task = await tasks_crud.get_task_by_id(session=session, task_id=test_task.task_id)
    # if task.type.base_type.id == 1:
    #     correct_answer = task.answer_data["max_flow"]
    #     if correct_answer == int(ttr.answer.data):
    #         return True
    return False
