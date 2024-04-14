import logging
from typing import List
from api.scr.app.core import models as dbm
from api.scr.app.variant_result_info import schemas as sch


logger = logging.getLogger(__name__)


def make_variant_result_info(
    vris: List[dbm.VariantResultInfo],
) -> List[sch.VariantResultInfo]:
    logger.debug(f"HANDLERS Making variant result info...")
    result = []
    for vr in vris:
        result.append(sch.VariantResultInfo.model_validate(vr))
    return result
