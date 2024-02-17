from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from scr.app.database import get_async_session
from scr.app.tasks.models import TaskType
from scr.app.tasks.schemas import TastTypeCreate

router = APIRouter(
    prefix="/task_types",
    tags=["Task types"]
)

@router.get("")
async def get_all_task_types(session: AsyncSession = Depends(get_async_session)) -> List[TastTypeCreate]:
    try:
        query = select(TaskType)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })
    
@router.get("/{task_type_id}")
async def get_all_task_types(task_type_id: int, session: AsyncSession = Depends(get_async_session)) -> TastTypeCreate:
    try:
        query = select(TaskType).where(TaskType.id == task_type_id)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("")
async def add_task_type(new_task_type: TastTypeCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Добавление типа задания в БД
    """
    query = insert(TaskType).values(**new_task_type.dict())
    await session.execute(query)
    await session.commit()
    return {"status": "success"}
