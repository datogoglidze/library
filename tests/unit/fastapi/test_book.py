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

    response = client.post(
        "/books",
        json=book,
    )

    assert response.status_code == 201, response.json()
    assert response.json() == {"id": ANY, **book}

    shelf.clear()


@pytest.mark.skip
def test_read_all_books() -> None:
    client.post(
        "/books",
        json={
            "title": title,
            "author": author,
            "isbn": isbn,
            "publisher": publisher,
            "total_pages": total_pages,
            "year": year,
        },
    )
    client.post(
        "/books",
        json={
            "title": str(Faker().job()),
            "author": str(Faker().first_name()),
            "isbn": str(Faker().isbn13()),
            "publisher": str(Faker().company()),
            "total_pages": int(Faker().random_digit_not_null() * 10),
            "year": int(Faker().year()),
        },
    )

    response = client.get("/books")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": ANY,
            "title": str(Faker().job()),
            "author": str(Faker().first_name()),
            "isbn": str(Faker().isbn13()),
            "publisher": str(Faker().company()),
            "total_pages": int(Faker().random_digit_not_null() * 10),
            "year": int(Faker().year()),
        },
        {
            "id": ANY,
            "title": str(Faker().job()),
            "author": str(Faker().first_name()),
            "isbn": str(Faker().isbn13()),
            "publisher": str(Faker().company()),
            "total_pages": int(Faker().random_digit_not_null() * 10),
            "year": int(Faker().year()),
        },
    ]

    shelf.clear()


@pytest.mark.skip
def test_read_one_book() -> None:
    uuid = Faker().uuid4()
    first_book = create_book()
    second_book = create_book()
    client.post("/books", json=first_book)
    client.post("/books", json=second_book)

    response = client.get(f"/books/{uuid}")

    assert response.status_code == 200, response.json()
    assert response.json() == first_book

    shelf.clear()


@pytest.mark.skip
def test_not_read_missing() -> None:
    book = create_book()
    client.post("/books", json=book)

    response = client.get(f"/books/{Faker().uuid4()}")

    assert response.status_code == 404
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
