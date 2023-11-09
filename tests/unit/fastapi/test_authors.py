from unittest.mock import ANY

from tests.client import FirstlibApi
from tests.unit.fastapi.fake import Fake

fake = Fake()


def test_should_create(firstlib: FirstlibApi) -> None:
    author = fake.author()

    firstlib.authors.create_one(
        from_data=author,
    ).assert_created(
        author={"id": ANY, **author},
    )


def test_should_not_duplicate(firstlib: FirstlibApi) -> None:
    author = firstlib.authors.create_one(fake.author())

    firstlib.authors.create_one(
        from_data=author.unpack(exclude=["id"]),
    ).assert_conflict(
        with_message=f"Author with name<{author['name']}> already exists.",
        and_data={"author": {"id": author["id"]}},
    )


def test_should_list_all_created(firstlib: FirstlibApi) -> None:
    authors = [
        firstlib.authors.create_one(fake.author()).unpack(),
        firstlib.authors.create_one(fake.author()).unpack(),
    ]

    firstlib.authors.read_all().assert_ok(authors=authors, count=len(authors))


def test_should_read_one(firstlib: FirstlibApi) -> None:
    author = firstlib.authors.create_one(fake.author())

    firstlib.authors.read_one(with_id=author["id"]).assert_ok(author=author.unpack())


def test_should_not_list_anything_when_none_exists(firstlib: FirstlibApi) -> None:
    firstlib.authors.read_all().assert_ok(authors=[], count=0)


def test_should_not_read_unknown(firstlib: FirstlibApi) -> None:
    unknown_author_id = fake.uuid()

    firstlib.authors.read_one(
        with_id=unknown_author_id,
    ).assert_not_found(
        with_message=f"Author with id<{unknown_author_id}> does not exist.",
    )
