import logging
from typing import List
from api.scr.app.core import models as dbm
from api.scr.app.variants_task_result import schemas as sch


logger = logging.getLogger(__name__)


def make_variant_task_result(
    vris: List[dbm.VariantsTaskResult],
) -> List[sch.VariantTaskResult]:
    logger.debug(f"HANDLERS Making variant task result...")
    result = []
    for vr in vris:
        if vr is None:
            continue
        result.append(sch.VariantTaskResult.model_validate(vr))
    return result
