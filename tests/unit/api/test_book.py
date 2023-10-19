from faker import Faker
from fastapi.testclient import TestClient

from firstlib.api.book import app

client = TestClient(app)

book_info = {
    "book_id": Faker().uuid4(),
    "title": str(Faker().job()),
    "author": str(Faker().first_name()),
    "isbn": str(Faker().isbn13()),
    "publisher": str(Faker().company()),
    "total_pages": int(Faker().random_digit_not_null() * 10),
    "year": int(Faker().year()),
}


def test_create_book() -> None:
    response = client.post("/books", json=book_info)

    assert response.status_code == 201, response.json()
    assert response.json() == book_info


def test_read_all_books() -> None:
    response = client.get("/books")

    assert response.status_code == 200
    assert response.json() == [book_info]


def test_read_one_book() -> None:
    uuid = Faker().uuid4()
    book_info = {
        "book_id": uuid,
        "title": str(Faker().job()),
        "author": str(Faker().first_name()),
        "isbn": str(Faker().isbn13()),
        "publisher": str(Faker().company()),
        "total_pages": int(Faker().random_digit_not_null() * 10),
        "year": int(Faker().year()),
    }
    client.post(
        "/books",
        json=book_info,
    )
    response = client.get(f"/books/{uuid}")

    assert response.status_code == 200, response.json()
    assert response.json() == book_info
