from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from firstlib.infra.fastapi.docs import Response
from firstlib.infra.fastapi.response import (
    ResourceCreated,
    ResourceExists,
    ResourceFound,
    ResourceNotFound,
)

books_api = APIRouter(tags=["Books"])

shelf: list[dict[str, Any]] = []


class BookCreateRequest(BaseModel):
    name: str
    author: str
    isbn: str
    publisher: str
    total_pages: int
    year: int


class BookItem(BaseModel):
    id: UUID
    name: str
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
def create(request: BookCreateRequest) -> JSONResponse | dict[str, Any]:
    book = {
        "id": uuid4(),
        "name": request.name,
        "author": request.author,
        "isbn": request.isbn,
        "publisher": request.publisher,
        "total_pages": request.total_pages,
        "year": request.year,
    }

    for book_info in shelf:
        if book_info["isbn"] == book["isbn"]:
            return ResourceExists(
                f"Book with ISBN<{book_info['isbn']}> already exists.",
                book={"id": str(book_info["id"])},
            )

    shelf.append(book)

    return ResourceCreated(book=book)


@books_api.get(
    "",
    status_code=200,
    response_model=Response[BookListEnvelope],
)
def read_all() -> ResourceFound:
    return ResourceFound(books=shelf, count=len(shelf))


@books_api.get(
    "/{book_id}",
    status_code=200,
    response_model=Response[BookItemEnvelope],
)
def read_one(book_id: UUID) -> ResourceFound | ResourceNotFound:
    for book_info in shelf:
        if book_info["id"] == book_id:
            return ResourceFound(book=book_info)

    return ResourceNotFound(f"Book with id<{book_id}> does not exist.")
