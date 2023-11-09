from unittest.mock import ANY

import pytest
from pydevtools.http import Httpx
from pydevtools.testing import RestfulName, RestResource

from tests.unit.fastapi.fake import Fake

fake = Fake()


@pytest.fixture
def publishers_api(http: Httpx) -> RestResource:
    return RestResource(http, RestfulName("publisher"))


def test_should_create(publishers_api: RestResource) -> None:
    publisher = fake.publisher()

    (
        publishers_api.create_one()
        .from_data(publisher)
        .ensure()
        .success()
        .with_code(201)
        .with_data(publisher={"id": ANY, **publisher})
    )


def test_should_not_duplicate(publishers_api: RestResource) -> None:
    publisher = fake.publisher()
    publishers_api.create_one().from_data(publisher).unpack()

    (
        publishers_api.create_one()
        .from_data(publisher)
        .ensure()
        .fail()
        .with_code(409)
        .and_message(f"Publisher with name<{publisher['name']}> already exists.")
        .and_data(publisher={"id": ANY})
    )


def test_should_list_all_created(publishers_api: RestResource) -> None:
    publishers = [
        dict(publishers_api.create_one().from_data(fake.publisher()).unpack()),
        dict(publishers_api.create_one().from_data(fake.publisher()).unpack()),
    ]

    (
        publishers_api.read_all()
        .ensure()
        .success()
        .with_code(200)
        .and_data(publishers=publishers, count=len(publishers))
    )


def test_should_read_one(publishers_api: RestResource) -> None:
    publisher = fake.publisher()
    id_ = (
        publishers_api.create_one().from_data(publisher).unpack().value_of("id").to(str)
    )

    (
        publishers_api.read_one()
        .with_id(id_)
        .ensure()
        .success()
        .with_code(200)
        .and_data(publisher={"id": id_, **publisher})
    )


def test_should_not_list_anything_when_none_exists(
    publishers_api: RestResource,
) -> None:
    (
        publishers_api.read_all()
        .ensure()
        .success()
        .with_code(200)
        .and_data(publishers=[], count=0)
    )


def test_should_not_read_unknown(publishers_api: RestResource) -> None:
    unknown_publisher_id = fake.uuid()

    (
        publishers_api.read_one()
        .with_id(unknown_publisher_id)
        .ensure()
        .fail()
        .with_code(404)
        .and_message(f"Publisher with id<{unknown_publisher_id}> does not exist.")
    )
