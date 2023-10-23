from unittest.mock import ANY

from fastapi.testclient import TestClient

from firstlib.infra.fastapi import FastApiConfig
from firstlib.infra.fastapi.books import shelf
from tests.unit.fastapi.fake import Fake

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


def test_should_not_read_missing() -> None:
    book = fake.book()
    client.post("/books", json=book)

    response = client.get(f"/books/{fake.uuid()}")

    assert response.status_code == 404, response.json()
    assert response.json()["detail"] == "Book not found"

    shelf.clear()


def test_should_not_add_existing() -> None:
    book = fake.book()
    client.post("/books", json=book)

    response = client.post("/books", json=book)

    assert response.status_code == 409
    assert response.json()["detail"] == "Book already exists"

    shelf.clear()