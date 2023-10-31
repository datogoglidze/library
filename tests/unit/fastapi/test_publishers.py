from unittest.mock import ANY

import pytest
from fastapi.testclient import TestClient

from firstlib.infra.fastapi import FastApiConfig
from firstlib.infra.fastapi.publishers import all_publishers
from tests.client import RestfulName, RestResource
from tests.unit.fastapi.fake import Fake

fake = Fake()


@pytest.fixture
def publishers() -> RestResource:
    return RestResource(TestClient(FastApiConfig().setup()), RestfulName("publisher"))


def test_should_create(publishers: RestResource) -> None:
    publisher = fake.publisher()

    publishers.create_one(
        from_data=publisher,
    ).assert_created(
        publisher={"id": ANY, **publisher},
    )


def test_should_not_duplicate(publishers: RestResource) -> None:
    publisher = publishers.create_one(fake.publisher())

    publishers.create_one(
        from_data=publisher.unpack(exclude=["id"]),
    ).assert_conflict(
        with_message=f"Publisher with name<{publisher['name']}> already exists.",
        and_data={"publisher": {"id": publisher["id"]}},
    )


def test_should_list_all_created(publishers: RestResource) -> None:
    all_publishers.clear()

    fake_publishers = [
        publishers.create_one(fake.publisher()).unpack(),
        publishers.create_one(fake.publisher()).unpack(),
    ]

    publishers.read_all().assert_ok(
        publishers=fake_publishers, count=len(fake_publishers)
    )

    all_publishers.clear()


def test_should_read_one(publishers: RestResource) -> None:
    publisher = publishers.create_one(fake.publisher())

    publishers.read_one(with_id=publisher["id"]).assert_ok(publisher=publisher.unpack())


def test_should_not_list_anything_when_none_exists(publishers: RestResource) -> None:
    all_publishers.clear()

    publishers.read_all().assert_ok(publishers=[], count=0)


def test_should_not_read_unknown(publishers: RestResource) -> None:
    unknown_publisher_id = fake.uuid()

    publishers.read_one(
        with_id=unknown_publisher_id,
    ).assert_not_found(
        with_message=f"Publisher with id<{unknown_publisher_id}> does not exist.",
    )
