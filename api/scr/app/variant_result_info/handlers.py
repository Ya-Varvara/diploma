import logging
from typing import List
from api.scr.app.core import models as dbm
from api.scr.app.variant_result_info import schemas as sch


logger = logging.getLogger(__name__)


def make_variant_result_info(
    vris: List[dbm.VariantResultInfo],
) -> List[sch.VariantResultInfo]:
    logger.debug(f"HANDLERS Making variant result info for {vris}...")
    result = []
    for vr in vris:
        if vr is None:
            continue
        result.append(sch.VariantResultInfo.model_validate(vr))
    return result
