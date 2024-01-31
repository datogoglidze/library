from unittest.mock import ANY

import pytest
from pydevtools.http import Httpx
from pydevtools.testing import RestfulName, RestResource

from tests.unit.fastapi.fake import Fake

fake = Fake()


@pytest.fixture
def books_api(http: Httpx) -> RestResource:
    return RestResource(http, RestfulName("book"))


@pytest.fixture
def author_id(http: Httpx) -> str:
    return str(
        RestResource(http, RestfulName("author"))
        .create_one()
        .from_data(fake.author())
        .unpack()
        .value_of("id")
        .to(str)
    )


@pytest.fixture
def publisher_id(http: Httpx) -> str:
    return str(
        RestResource(http, RestfulName("publisher"))
        .create_one()
        .from_data(fake.publisher())
        .unpack()
        .value_of("id")
        .to(str)
    )


def test_should_create(
    books_api: RestResource,
    author_id: str,
    publisher_id: str,
) -> None:
    book = fake.book(author_id, publisher_id)

    (
        books_api.create_one()
        .from_data(book)
        .ensure()
        .success()
        .with_code(201)
        .and_data(book.with_a(id=ANY))
    )


def test_should_not_duplicate(
    books_api: RestResource,
    author_id: str,
    publisher_id: str,
) -> None:
    book = books_api.create_one().from_data(fake.book(author_id, publisher_id)).unpack()
    book_isbn = book.value_of("isbn").to(str)

    (
        books_api.create_one()
        .from_data(book)
        .ensure()
        .fail()
        .with_code(409)
        .and_message(f"Book with ISBN<{book_isbn}> already exists.")
        .and_data(book.select("id"))
    )


def test_should_list_all_created(
    books_api: RestResource,
    author_id: str,
    publisher_id: str,
) -> None:
    books = [
        books_api.create_one().from_data(fake.book(author_id, publisher_id)).unpack(),
        books_api.create_one().from_data(fake.book(author_id, publisher_id)).unpack(),
    ]

    books_api.read_all().ensure().success().with_code(200).and_data(*books)


def test_should_read_one(
    books_api: RestResource,
    author_id: str,
    publisher_id: str,
) -> None:
    book = books_api.create_one().from_data(fake.book(author_id, publisher_id)).unpack()

    (
        books_api.read_one()
        .with_id(book.value_of("id").to(str))
        .ensure()
        .success()
        .with_code(200)
        .and_data(book)
    )


def test_should_not_list_anything_when_none_exists(books_api: RestResource) -> None:
    books_api.read_all().ensure().success().with_code(200).and_data()


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


def test_create_with_author(
    books_api: RestResource,
    author_id: str,
    publisher_id: str,
) -> None:
    book = fake.book(author_id, publisher_id)

    (
        books_api.create_one()
        .from_data(book)
        .ensure()
        .success()
        .with_code(201)
        .and_data(book.with_a(id=ANY))
    )


def test_should_not_create_with_unknown_author(
    books_api: RestResource,
    publisher_id: str,
) -> None:
    unknown_author_id = fake.uuid()
    book = fake.book(unknown_author_id, publisher_id)

    (
        books_api.create_one()
        .from_data(book)
        .ensure()
        .fail()
        .with_code(404)
        .with_message(f"Author with id<{unknown_author_id}> does not exist.")
    )


def test_create_with_publisher(
    books_api: RestResource,
    author_id: str,
    publisher_id: str,
) -> None:
    book = fake.book(author_id, publisher_id)

    (
        books_api.create_one()
        .from_data(book)
        .ensure()
        .success()
        .with_code(201)
        .and_data(book.with_a(id=ANY))
    )


def test_should_not_create_with_unknown_publisher(
    books_api: RestResource,
    author_id: str,
) -> None:
    unknown_publisher_id = fake.uuid()
    book = fake.book(author_id, unknown_publisher_id)

    (
        books_api.create_one()
        .from_data(book)
        .ensure()
        .fail()
        .with_code(404)
        .with_message(f"Publisher with id<{unknown_publisher_id}> does not exist.")
    )
