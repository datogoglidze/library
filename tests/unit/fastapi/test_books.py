from unittest.mock import ANY

import pytest
from pydevtools.http import Httpx
from pydevtools.testing import RestfulName, RestResource

from tests.unit.fastapi.fake import Fake

fake = Fake()


@pytest.fixture
def books_api(http: Httpx) -> RestResource:
    return RestResource(http, RestfulName("book"))


def test_should_create(books_api: RestResource) -> None:
    book = fake.book()

    (
        books_api.create_one()
        .from_data(book)
        .ensure()
        .success()
        .with_code(201)
        .with_data(book={"id": ANY, **book})
    )


def test_should_not_duplicate(books_api: RestResource) -> None:
    book = fake.book()
    books_api.create_one().from_data(book).unpack()

    (
        books_api.create_one()
        .from_data(book)
        .ensure()
        .fail()
        .with_code(409)
        .and_message(f"Book with ISBN<{book['isbn']}> already exists.")
        .and_data(book={"id": ANY})
    )


def test_should_list_all_created(books_api: RestResource) -> None:
    books = [
        dict(books_api.create_one().from_data(fake.book()).unpack()),
        dict(books_api.create_one().from_data(fake.book()).unpack()),
    ]

    (
        books_api.read_all()
        .ensure()
        .success()
        .with_code(200)
        .and_data(books=books, count=len(books))
    )


def test_should_read_one(books_api: RestResource) -> None:
    book = fake.book()
    id_ = books_api.create_one().from_data(book).unpack().value_of("id").to(str)

    (
        books_api.read_one()
        .with_id(id_)
        .ensure()
        .success()
        .with_code(200)
        .and_data(book={"id": id_, **book})
    )


def test_should_not_list_anything_when_none_exists(books_api: RestResource) -> None:
    (books_api.read_all().ensure().success().with_code(200).and_data(books=[], count=0))


def test_should_not_read_unknown(books_api: RestResource) -> None:
    unknown_book_id = fake.uuid()

    (
        books_api.read_one()
        .with_id(unknown_book_id)
        .ensure()
        .fail()
        .with_code(404)
        .and_message(f"Book with id<{unknown_book_id}> does not exist.")
    )
