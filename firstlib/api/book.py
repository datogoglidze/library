from dataclasses import dataclass
from typing import Any
from uuid import UUID

from fastapi import FastAPI, HTTPException
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


JsonDict = dict[str, Any]
shelf: list[JsonDict] = []


@app.post("/books", status_code=201)
def create_book(book: Book) -> JsonDict:
    book_info = {
        "book_id": book.book_id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "publisher": book.publisher,
        "total_pages": book.total_pages,
        "year": book.year,
    }

    for each_book in shelf:
        if (
            each_book["book_id"] == book_info["book_id"]
            and each_book["title"] == book_info["title"]
            and each_book["author"] == book_info["author"]
            and each_book["isbn"] == book_info["isbn"]
        ):
            raise HTTPException(status_code=409, detail="Book already exists")

    shelf.append(book_info)

    return book_info


@app.get("/books", status_code=200)
def show_shelf() -> list[JsonDict]:
    return shelf


@app.get("/books/{book_id}", status_code=200)
def show_one(book_id: UUID) -> JsonDict:
    for book_info in shelf:
        if book_info["book_id"] == book_id:
            return book_info
    raise HTTPException(status_code=404, detail="Book not found")
