import logging

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.database import get_async_session
from api.scr.app.core import models as dbm

from api.scr.app.variants import crud
from api.scr.app.variants import schemas as sch
from api.scr.app.variants import handlers

from api.scr.app.tests.crud import get_test_by_link

from api.scr.app.auth.router import get_current_user

from api.scr.app.variant_result_info.crud import add_variant_result_info
from api.scr.app.variants_task_result.crud import add_variant_task_result


router = APIRouter(prefix="/variant", tags=["Variant"])
logger = logging.getLogger(__name__)


@router.get("/{test_id}/", response_model=List[sch.VariantForTeacher])
async def get_all_variants_for_test(
    test_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
):
    logger.debug(
        f"ROUTER Getting all variant for test with id={test_id} for user with id={user.id}"
    )
    options = {"user_id": user.id}
    variants = await crud.get_all_variants_for_test(
        session=session, test_id=test_id, **options
    )
    return handlers.make_variant_for_teacher(variants=variants)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=sch.VariantForStudent,
)
async def get_variant_for_student(
    link: str, session: AsyncSession = Depends(get_async_session)
):
    logger.debug(f"ROUTER Getting variant by link={link}")
    test = await get_test_by_link(session=session, test_link=link)
    variant = await crud.get_variant_for_test(session=session, test_id=test.id)
    if variant is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Test variant not found",
        )
    logger.debug(f"ROUTER Making variant with id={variant.id} given")
    await crud.make_test_variant_given(session=session, test_variant_id=variant.id)
    return handlers.make_variant_for_student([variant])[0]


@router.post(
    "/result/",
    status_code=status.HTTP_200_OK,
    # response_model=sch.VariantForStudent,
)
async def post_variant_results(
    variant_result: sch.VariantResultCreate,
    session: AsyncSession = Depends(get_async_session),
):
    logger.debug(f"ROUTER Posting variant's result from student...")
    await add_variant_result_info(session=session, info_in=variant_result.info)

    for r in variant_result.answers:
        await add_variant_task_result(session=session, task_result_in=r)

    return
