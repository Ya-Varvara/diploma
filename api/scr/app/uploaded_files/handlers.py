import logging
from typing import List
from api.scr.app.core import models as dbm
from api.scr.app.uploaded_files import schemas as sch


logger = logging.getLogger(__name__)


def make_uploaded_files_info(
    upfs: List[dbm.UploadedFile],
) -> List[sch.UploadedFile]:
    logger.debug(f"HANDLERS Making uploaded file infos...")
    result = []
    for info in upfs:
        if info is None:
            continue
        result.append(
            sch.UploadedFile(
                name=info.name,
                path=info.path,
                variant_id=info.variant_id,
                id=info.id,
                upload_date=info.upload_date,
            )
        )
    return result
