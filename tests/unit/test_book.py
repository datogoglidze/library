from fastapi.testclient import TestClient

from firstlib.book import app, shelf

client = TestClient(app)


def test_create_book():
    response = client.post(
        "/books",
        json={
            "title": "LOTR",
            "author": "Tolkien",
        },
    )

    assert response.status_code == 201, response.json()
    assert response.json() == {
        "title": "LOTR",
        "author": "Tolkien",
    }

    shelf.clear()


def test_read_book():
    client.post(
        "/books",
        json={
            "title": "LOTR",
            "author": "Tolkien",
        },
    )
    response = client.get("/books")

    assert response.status_code == 200
    assert response.json() == {
        "shelf": [
            {
                "title": "LOTR",
                "author": "Tolkien",
            }
        ]
    }

    shelf.clear()
