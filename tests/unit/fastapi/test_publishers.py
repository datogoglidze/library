from unittest.mock import ANY

from firstlib.infra.fastapi.publishers import all_publishers
from tests.client import FirstlibApi
from tests.unit.fastapi.fake import Fake

fake = Fake()


def test_should_create(firstlib: FirstlibApi) -> None:
    publisher = fake.publisher()

    firstlib.publishers.create_one(
        from_data=publisher,
    ).assert_created(
        publisher={"id": ANY, **publisher},
    )


def test_should_not_duplicate(firstlib: FirstlibApi) -> None:
    publisher = firstlib.publishers.create_one(fake.publisher())

    firstlib.publishers.create_one(
        from_data=publisher.unpack(exclude=["id"]),
    ).assert_conflict(
        with_message=f"Publisher with name<{publisher['name']}> already exists.",
        and_data={"publisher": {"id": publisher["id"]}},
    )


def test_should_list_all_created(firstlib: FirstlibApi) -> None:
    all_publishers.clear()

    fake_publishers = [
        firstlib.publishers.create_one(fake.publisher()).unpack(),
        firstlib.publishers.create_one(fake.publisher()).unpack(),
    ]

    firstlib.publishers.read_all().assert_ok(
        publishers=fake_publishers, count=len(fake_publishers)
    )

    all_publishers.clear()


def test_should_read_one(firstlib: FirstlibApi) -> None:
    publisher = firstlib.publishers.create_one(fake.publisher())

    firstlib.publishers.read_one(with_id=publisher["id"]).assert_ok(
        publisher=publisher.unpack()
    )


def test_should_not_list_anything_when_none_exists(firstlib: FirstlibApi) -> None:
    all_publishers.clear()

    firstlib.publishers.read_all().assert_ok(publishers=[], count=0)


def test_should_not_read_unknown(firstlib: FirstlibApi) -> None:
    unknown_publisher_id = fake.uuid()

    firstlib.publishers.read_one(
        with_id=unknown_publisher_id,
    ).assert_not_found(
        with_message=f"Publisher with id<{unknown_publisher_id}> does not exist.",
    )
