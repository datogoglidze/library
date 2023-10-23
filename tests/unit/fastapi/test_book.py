from typing import Any
from uuid import UUID

from faker import Faker
from fastapi.testclient import TestClient

from firstlib.infra.fastapi.book import app, shelf

client = TestClient(app)


def test_create_book() -> None:
    book = create_book(Faker().uuid4())

    response = client.post("/books", json=book)

    assert response.status_code == 201, response.json()
    assert response.json() == book

    shelf.clear()


def test_read_all_books() -> None:
    first_book = create_book(Faker().uuid4())
    second_book = create_book(Faker().uuid4())
    client.post("/books", json=first_book)
    client.post("/books", json=second_book)

    response = client.get("/books")

    assert response.status_code == 200
    assert response.json() == [first_book, second_book]

    shelf.clear()


def test_read_one_book() -> None:
    uuid = Faker().uuid4()
    first_book = create_book(uuid)
    second_book = create_book(Faker().uuid4())
    client.post("/books", json=first_book)
    client.post("/books", json=second_book)

    response = client.get(f"/books/{uuid}")

    assert response.status_code == 200, response.json()
    assert response.json() == first_book

    shelf.clear()


def test_not_read_missing() -> None:
    book = create_book(Faker().uuid4())
    client.post("/books", json=book)

    response = client.get(f"/books/{Faker().uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

    shelf.clear()


def test_should_not_add_existing() -> None:
    book = create_book(Faker().uuid4())
    client.post("/books", json=book)

    response = client.post("/books", json=book)

    assert response.status_code == 409
    assert response.json()["detail"] == "Book already exists"

    shelf.clear()


def create_book(uuid: UUID) -> dict[str, Any]:
    return {
        "book_id": uuid,
        "title": str(Faker().job()),
        "author": str(Faker().first_name()),
        "isbn": str(Faker().isbn13()),
        "publisher": str(Faker().company()),
        "total_pages": int(Faker().random_digit_not_null() * 10),
        "year": int(Faker().year()),
    }
