from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from firstlib.infra.fastapi.docs import Response
from firstlib.infra.fastapi.response import ResourceCreated, ResourceFound

books_api = APIRouter(tags=["Books"])

shelf: list[dict[str, Any]] = []


class BookCreateRequest(BaseModel):
    title: str
    author: str
    isbn: str
    publisher: str
    total_pages: int
    year: int


class BookItem(BaseModel):
    id: UUID
    title: str
    author: str
    isbn: str
    publisher: str
    total_pages: int
    year: int


class BookItemEnvelope(BaseModel):
    book: BookItem


class BookListEnvelope(BaseModel):
    count: int
    books: list[BookItem]


@books_api.post(
    "",
    status_code=201,
    response_model=Response[BookItemEnvelope],
)
def create_book(request: BookCreateRequest) -> ResourceCreated:
    book_info = {
        "id": uuid4(),
        "title": request.title,
        "author": request.author,
        "isbn": request.isbn,
        "publisher": request.publisher,
        "total_pages": request.total_pages,
        "year": request.year,
    }

    for each_book in shelf:
        if each_book["isbn"] == book_info["isbn"]:
            raise HTTPException(status_code=409, detail="Book already exists")

    shelf.append(book_info)

    return ResourceCreated(book=book_info)


@books_api.get(
    "",
    status_code=200,
    response_model=Response[BookListEnvelope],
)
def read_all() -> ResourceFound:
    return ResourceFound(books=shelf, count=len(shelf))


@books_api.get("/{id}", status_code=200)
def show_one(id: UUID) -> dict[str, Any]:
    for book_info in shelf:
        if book_info["id"] == id:
            return book_info
    raise HTTPException(status_code=404, detail="Book not found")
