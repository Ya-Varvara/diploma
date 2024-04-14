import logging
from typing import List
from datetime import datetime
from uuid import uuid4

from api.scr.app.core import models as dbm

from api.scr.app.tests import schemas as sch
from api.scr.app.task_types.handlers import make_full_task_type


logger = logging.getLogger(__name__)


def make_new_test_data(test_in: sch.TestCreate, **options) -> dbm.Test:
    logger.debug(f"HANDLERS Making new test data...")
    test_data = test_in.model_dump(
        exclude={"task_types", "start_datetime", "end_datetime", "test_time"}
    )

    test_data["start_datetime"] = test_in.start_datetime.replace(tzinfo=None)
    test_data["end_datetime"] = test_in.end_datetime.replace(tzinfo=None)
    test_data["test_time"] = test_in.test_time.replace(tzinfo=None)

    test_data["user_id"] = options.get("user_id", 1)
    test_data["link"] = str(uuid4())
    test_data["created_at"] = datetime.now()
    test_data["updated_at"] = datetime.now()
    test_data["deleted"] = False

    logger.debug(f"HANDLERS New test data {test_data}")

    return dbm.Test(**test_data)


def make_full_test(tests: List[dbm.Test]) -> List[sch.FullTest]:
    logger.debug(f"HANDLERS Making full test's data...")
    result = []
    for test in tests:
        newtest = sch.FullTest(
            name=test.name,
            start_datetime=test.start_datetime,
            end_datetime=test.end_datetime,
            test_time=test.test_time,
            variants_number=test.variants_number,
            id=test.id,
            user_id=test.user_id,
            link=test.link,
            upload=test.upload,
            created_at=test.created_at,
            updated_at=test.updated_at,
            deleted=test.deleted,
            task_types=[
                sch.TaskTypesForFullTest(
                    type=make_full_task_type([t.task_type])[0], number=t.number
                )
                for t in test.task_types
            ],
        )
        result.append(newtest)
    logger.debug(f"HANDLERS Full test's data {result}")
    return result


def make_test_data_for_variant(
    test_infos: List[dbm.Test],
) -> List[sch.TestDataForVariant]:
    logger.debug(f"HANDLERS Making test data for variant...")
    result = []
    for data in test_infos:
        new = sch.TestDataForVariant(
            test_id=data.id,
            name=data.name,
            start_datetime=data.start_datetime,
            end_datetime=data.end_datetime,
            test_time=data.test_time,
            upload=data.upload,
        )
        result.append(new)
    return result
