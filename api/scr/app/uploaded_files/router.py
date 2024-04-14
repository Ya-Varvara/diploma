from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.database import get_async_session

from api.scr.app.uploaded_files import crud
from api.scr.app.uploaded_files import schemas as sch


router = APIRouter(prefix="/upload", tags=["Upload files"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=sch.UploadedFile)
async def upload_file(
    variant_id: int,
    session: AsyncSession = Depends(get_async_session),
    file: UploadFile = File(...),
):
    logger.debug(f"ROUTER Adding file for variant {variant_id}")
    file_location = f"files/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return await crud.create_file(
        session=session,
        file_in=sch.UploadedFileCreate(
            name=file.filename, path=file_location, variant_id=variant_id
        ),
    )


@router.get("/{file_id}/")
async def get_file(
    file_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    logger.debug(f"ROUTER Getting file with id={file_id}")
    file_data = await crud.get_file_by_id(session=session, file_id=file_id)
    if file_data:
        return FileResponse(path=file_data.path, filename=file_data.name)
    else:
        raise HTTPException(status_code=404, detail="File not found")
