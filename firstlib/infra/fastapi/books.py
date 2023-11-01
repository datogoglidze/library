from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter, Request, Depends
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


def get_book_repository(request: Request) -> list[dict[str, Any]]:
    return request.app.state.books


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
def create(
    request: BookCreateRequest,
    books: list[dict[str, Any]] = Depends(get_book_repository),
) -> JSONResponse | dict[str, Any]:
    book = {
        "id": uuid4(),
        "name": request.name,
        "author": request.author,
        "isbn": request.isbn,
        "publisher": request.publisher,
        "total_pages": request.total_pages,
        "year": request.year,
    }

    for book_info in books:
        if book_info["isbn"] == book["isbn"]:
            return ResourceExists(
                f"Book with ISBN<{book_info['isbn']}> already exists.",
                book={"id": str(book_info["id"])},
            )

    books.append(book)

    return ResourceCreated(book=book)


@books_api.get(
    "",
    status_code=200,
    response_model=Response[BookListEnvelope],
)
def read_all(
    books: list[dict[str, Any]] = Depends(get_book_repository),
) -> ResourceFound:
    return ResourceFound(books=books, count=len(books))


@books_api.get(
    "/{book_id}",
    status_code=200,
    response_model=Response[BookItemEnvelope],
)
def read_one(
    book_id: UUID,
    books: list[dict[str, Any]] = Depends(get_book_repository),
) -> ResourceFound | ResourceNotFound:
    for book_info in books:
        if book_info["id"] == book_id:
            return ResourceFound(book=book_info)

    return ResourceNotFound(f"Book with id<{book_id}> does not exist.")
