from unittest.mock import ANY

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from firstlib.infra.fastapi import FastApiConfig
from firstlib.infra.fastapi.bookcreaterequest import shelf
from firstlib.infra.fastapi.fake import Fake

fake = Fake()
client = TestClient(FastApiConfig().setup())


def test_create_book() -> None:
    book = fake.book()

    response = client.post("/books", json=book)

    assert response.status_code == 201, response.json()
    assert response.json() == {"id": ANY, **book}

    shelf.clear()


def test_read_all_books() -> None:
    book_one = fake.book()
    book_two = fake.book()

    client.post("/books", json=book_one)
    client.post("/books", json=book_two)
    response = client.get("/books")

    assert response.status_code == 200
    assert response.json() == [
        {"id": ANY, **book_one},
        {"id": ANY, **book_two},
    ]

    shelf.clear()


@pytest.mark.skip
def test_read_one_book() -> None:
    book_one = fake.book()
    book_two = fake.book()
    client.post("/books", json=book_one)
    client.post("/books", json=book_two)

    response = client.get(f"/books/{book_one['id']}")

    assert response.status_code == 200, response.json()
    assert response.json() == book_one

    shelf.clear()


def test_not_read_missing() -> None:
    book = fake.book()
    client.post("/books", json=book)

    response = client.get(f"/books/{fake.uuid()}")

    assert response.status_code == 404, response.json()
    assert response.json()["detail"] == "Book not found"

    shelf.clear()


@pytest.mark.skip
def test_should_not_add_existing() -> None:
    book = create_book()
    client.post("/books", json=book)

    response = client.post("/books", json=book)

    assert response.status_code == 409
    assert response.json()["detail"] == "Book already exists"

    shelf.clear()
