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


def make_new_variant_result_info(res_in: sch.VariantResultInfoCreate, **options) -> dbm.VariantResultInfo:
    logger.debug(f"HANDLERS Making new variant result info...")
    data = res_in.model_dump(
        exclude={"start_datetime", "end_datetime"}
    )

    data["start_datetime"] = res_in.start_datetime.replace(tzinfo=None)
    data["end_datetime"] = res_in.end_datetime.replace(tzinfo=None)

    logger.debug(f"HANDLERS New variant result info {data}")

    return dbm.VariantResultInfo(**data)
