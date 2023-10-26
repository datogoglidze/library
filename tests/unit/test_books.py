from unittest.mock import ANY

import pytest
from fastapi.testclient import TestClient

from firstlib.infra.fastapi import FastApiConfig
from firstlib.infra.fastapi.books import shelf
from tests.unit.client import RestfulName, RestResource
from tests.unit.fake import Fake

fake = Fake()
client = TestClient(FastApiConfig().setup())


@pytest.fixture
def books() -> RestResource:
    return RestResource(TestClient(FastApiConfig().setup()), RestfulName("book"))


def test_should_create(books: RestResource) -> None:
    book = fake.book()

    books.create_one(
        from_data=book,
    ).assert_created(
        book={"id": ANY, **book},
    )

    shelf.clear()


def test_should_list_all_created(books: RestResource) -> None:
    fake_books = [
        books.create_one(fake.book()).unpack(),
        books.create_one(fake.book()).unpack(),
    ]

    books.read_all().assert_ok(books=fake_books, count=len(fake_books))


def test_should_not_duplicate(books: RestResource) -> None:
    book = books.create_one(fake.book())

    books.create_one(
        from_data=book.unpack(exclude=["id"]),
    ).assert_conflict(with_message=f"Book with ISBN<{book['isbn']}> already exists.")


@pytest.mark.skip
def test_read_one_book() -> None:
    book_one = fake.book()
    book_two = fake.book()
    client.post("/books", json=book_one)
    client.post("/books", json=book_two)
    known_book_id = client.get("/books").json()[0]["id"]

    response = client.get(f"/books/{known_book_id}")

    assert response.status_code == 200, response.json()
    assert response.json() == {"id": ANY, **book_one}

    shelf.clear()


@pytest.mark.skip
def test_should_not_read_missing() -> None:
    book = fake.book()
    client.post("/books", json=book)

    response = client.get(f"/books/{fake.uuid()}")

    assert response.status_code == 404, response.json()
    assert response.json()["detail"] == "Book not found"

    shelf.clear()


@pytest.mark.skip
def test_should_not_add_existing() -> None:
    book = fake.book()
    client.post("/books", json=book)

    response = client.post("/books", json=book)

    assert response.status_code == 409
    assert response.json()["detail"] == "Book already exists"

    shelf.clear()
