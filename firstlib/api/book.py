from dataclasses import dataclass
from typing import Any
from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@dataclass
class Book(BaseModel):
    book_id: UUID
    title: str
    author: str
    isbn: str
    publisher: str
    total_pages: int
    year: int


shelf = []


@app.post("/books", status_code=201)
def create_book(book: Book) -> dict[str, Any]:
    book_info = {
        "book_id": book.book_id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "publisher": book.publisher,
        "total_pages": book.total_pages,
        "year": book.year,
    }

    shelf.append(book_info)

    return book_info


@app.get("/books", status_code=200)
def show_shelf() -> dict[str, list[dict[str, Any]]]:
    return {"shelf": shelf}
