"""
Create
Read
Update
Delete
"""

import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm

from api.scr.app.uploaded_files import schemas as sch


logger = logging.getLogger(__name__)


async def get_file_by_id(
    session: AsyncSession, file_id: int
) -> dbm.UploadedFile | None:
    stmt = select(dbm.UploadedFile).where(dbm.UploadedFile.id == file_id)
    file: dbm.UploadedFile | None = await session.scalar(stmt)
    return file


async def create_file(
    session: AsyncSession, file_in: sch.UploadedFileCreate, **options
) -> dbm.UploadedFile:
    logger.debug(f"CRUD New file creation for test variant id={file_in.variant_id}")
    file_data = file_in.model_dump()
    file_data["upload_date"] = datetime.now()
    file = dbm.UploadedFile(**file_data)
    session.add(file)
    await session.commit()
    return file
