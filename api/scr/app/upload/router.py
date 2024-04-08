from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
import shutil
from pathlib import Path
import os

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.database import get_async_session
from api.scr.app.forms import schemas as sch
from api.scr.app.core.models import User

from api.scr.app.auth.router import get_current_user

from api.scr.app.upload import crud
from api.scr.app.upload import schemas as sch

router = APIRouter(prefix="/upload", tags=["Upload files"])


@router.post("/", response_model=sch.UploadedFile)
async def upload_file(
    test_task_id: int,
    session: AsyncSession = Depends(get_async_session),
    file: UploadFile = File(...),
):
    file_location = f"files/{file.filename}"
    print(file_location)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return await crud.create_file(
        session=session,
        file_in=sch.UploadedFileCreation(
            name=file.filename, path=file_location, test_task_id=test_task_id
        ),
    )


@router.get("/{file_id}/")
async def get_file(
    file_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    file_data = await crud.get_file_by_id(session=session, file_id=file_id)
    if file_data:
        return FileResponse(path=file_data.path, filename=file_data.name)
    else:
        raise HTTPException(status_code=404, detail="File not found")
