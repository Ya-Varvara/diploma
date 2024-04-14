import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.scr.app.database import get_async_session
from api.scr.app.core import models as dbm

from api.scr.app.tests import crud
from api.scr.app.tests import schemas as sch
from api.scr.app.tests.handlers import make_full_test

from api.scr.app.auth.router import get_current_user


router = APIRouter(prefix="/test", tags=["Test"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[sch.FullTest])
async def get_tests(
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
):
    print("ROUTER GET TESTS")
    options = {"user_id": user.id}
    tests = await crud.get_tests(session=session, options=options)
    return make_full_test(tests)


@router.post(
    "/",
    response_model=sch.FullTest,
    status_code=status.HTTP_201_CREATED,
)
async def create_test(
    test_in: sch.TestCreate,
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
):
    logger.info(f"Create test from user {user.id}")
    options = {"user_id": user.id}
    test: dbm.Test = await crud.create_test(session=session, test_in=test_in, **options)
    return make_full_test([test])[0]


@router.get(
    "/{test_id}/",
    response_model=sch.FullTest,
)
async def get_test(
    test_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
):
    test = await crud.get_test_by_id(session=session, test_id=test_id, user_id=user.id)
    if test is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Test not found"
        )
    return make_full_test([test])[0]


@router.delete("/{test_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test(
    test_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: dbm.User = Depends(get_current_user()),
) -> None:
    test = await crud.get_test_by_id(session=session, test_id=test_id, user_id=user.id)
    if test is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Test not found"
        )
    await crud.delete_test(session=session, test=test)


# @router.get(
#     "/variant/{link}/",
#     status_code=status.HTTP_200_OK,
#     response_model=sch.TestVariant,
# )
# async def get_variant(link: str, session: AsyncSession = Depends(get_async_session)):
#     # test = await crud.get_test_by_link(session=session, link="test")
#     variant = await crud.get_free_variant_number(session=session, link=link)

#     if variant is None:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Test not found"
#         )

#     return await crud.get_test_by_link_and_variant(
#         session=session, link=link, variant=variant
#     )
