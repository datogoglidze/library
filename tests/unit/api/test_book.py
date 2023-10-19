from fastapi.testclient import TestClient

from firstlib.api.book import app, shelf

client = TestClient(app)


book = {
    "title": "LOTR",
    "author": "Tolkien",
}


def test_create_book() -> None:
    response = client.post("/books", json=book)

    assert response.status_code == 201, response.json()
    assert response.json() == book

    shelf.clear()


def test_read_book() -> None:
    client.post("/books", json=book)
    response = client.get("/books")

    assert response.status_code == 200
    assert response.json() == {"shelf": [book]}

    shelf.clear()
