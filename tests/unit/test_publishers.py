from unittest.mock import ANY

import pytest
from fastapi.testclient import TestClient

from firstlib.infra.fastapi import FastApiConfig
from firstlib.infra.fastapi.publishers import all_publishers
from tests.unit.client import RestfulName, RestResource
from tests.unit.fake import Fake

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

    all_publishers.clear()


def test_should_not_duplicate(publishers: RestResource) -> None:
    publisher = publishers.create_one(fake.publisher())

    publishers.create_one(
        from_data=publisher.unpack(exclude=["id"]),
    ).assert_conflict(
        with_message=f"Publisher with name<{publisher['name']}> already exists."
    )

    all_publishers.clear()


def test_should_list_all_created(publishers: RestResource) -> None:
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

    all_publishers.clear()


def test_should_not_read_unknown(publishers: RestResource) -> None:
    unknown_publisher_id = fake.uuid()

    publishers.read_one(
        with_id=unknown_publisher_id,
    ).assert_not_found(
        with_message=f"Publisher with id<{unknown_publisher_id}> does not exist.",
    )
