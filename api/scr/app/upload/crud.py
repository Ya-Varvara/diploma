"""
Create
Read
Update
Delete
"""

from random import choice
from typing import Any, List
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.core import models as dbm

from api.scr.app.upload import schemas as sch


async def get_file_by_id(
    session: AsyncSession, file_id: int
) -> dbm.UploadedFile | None:
    stmt = select(dbm.UploadedFile).where(dbm.UploadedFile.id == file_id)
    file: dbm.UploadedFile | None = await session.scalar(stmt)
    return file


async def create_file(
    session: AsyncSession, file_in: sch.UploadedFileCreation, **options
) -> dbm.UploadedFile:
    print("CRUD CREATE File")
    file_data = file_in.model_dump()
    file_data["upload_date"] = datetime.now()
    file = dbm.UploadedFile(**file_data)
    session.add(file)
    await session.commit()
    return file


async def delete_test(
    session: AsyncSession,
    file_id: int,
) -> None:
    pass