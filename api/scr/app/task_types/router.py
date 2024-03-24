from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.database import get_async_session
from api.scr.app.task_types import schemas as sch
from api.scr.app.forms import schemas as formsch
from api.scr.app.task_types.dependences import task_type_by_id

from api.scr.app.core import models as dbm

from api.scr.app.auth.router import get_current_user

import api.scr.app.task_types.crud as crud

router = APIRouter(prefix="/task_type", tags=["Task type"])


def make_full_task_type(task_types: List[dbm.TaskType]) -> List[sch.FullTaskType]:
    result = []
    for tt in task_types:
        # print(tt)
        # print(tt.__dict__)
        newtt = sch.FullTaskType(
            id=tt.id,
            name=tt.name,
            created_at=tt.created_at,
            updated_at=tt.updated_at,
            answer_forms=[formsch.Form.from_orm(af) for af in tt.answer_forms],
            condition_forms=[formsch.Form.from_orm(cf) for cf in tt.condition_forms],
            settings=tt.settings,
            base_task_type=tt.base_task_type,
            user_id=tt.user_id,
            deleted=tt.deleted,
        )
        # print(newtt.__dict__)
        result.append(newtt)
    return result


@router.get("/", response_model=List[sch.FullTaskType])
async def get_all_task_types(
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
):
    options = {"user_id": user.id}
    tts = await crud.get_all_task_types(session=session, options=options)
    return make_full_task_type(tts)


@router.get("/base_types/", response_model=List[sch.BaseTaskType])
async def get_all_base_task_types(
    session: AsyncSession = Depends(get_async_session),
):
    return await crud.get_all_base_task_types(session=session)


@router.post(
    "/",
    response_model=sch.FullTaskType,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_type(
    task_type_in: sch.TaskTypeCreate,
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
):
    tt = await crud.create_task_type(
        session=session, task_type_in=task_type_in, user_id=user.id
    )
    return make_full_task_type([tt])[0]


@router.get("/{task_type_id}/", response_model=sch.FullTaskType)
async def get_task_type_by_id(
    task_type_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
):
    options = {"user_id": user.id}
    task_type = await crud.get_task_type_by_id(
        session=session, task_type_id=task_type_id, options=options
    )
    if task_type is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task Type not found",
        )
    return make_full_task_type([task_type])[0]


# @router.put("/{task_type_id}/")
async def update_task_type(
    task_type_update: sch.TaskTypeUpdate,
    task_type: sch.TaskType = Depends(task_type_by_id),
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
):
    if task_type.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task Type not yours",
        )
    return await crud.update_task_type(
        session=session, task_type=task_type, task_type_update=task_type_update
    )


# @router.patch("/{task_type_id}/")
async def update_task_type_partial(
    task_type_update: sch.TaskTypeUpdatePartial,
    task_type: sch.TaskType = Depends(task_type_by_id),
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
):
    if task_type.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task Type not yours",
        )
    return await crud.update_task_type(
        session=session,
        task_type=task_type,
        task_type_update=task_type_update,
        partial=True,
    )


@router.delete("/{task_type_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_type(
    task_type: sch.TaskType = Depends(task_type_by_id),
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
) -> None:
    if task_type.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task Type not yours",
        )
    await crud.delete_task_type(session=session, task_type=task_type)
