from uuid import UUID, uuid4

from fastapi import APIRouter
from pydantic import BaseModel

from firstlib.core.book import Book
from firstlib.core.errors import DoesNotExistError, ExistsError
from firstlib.infra.fastapi.dependable import BookRepositoryDependable
from firstlib.infra.fastapi.docs import Response
from firstlib.infra.fastapi.response import (
    ResourceCreated,
    ResourceExists,
    ResourceFound,
    ResourceNotFound,
)

books_api = APIRouter(tags=["Books"])


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
    books: BookRepositoryDependable,
) -> ResourceCreated | ResourceExists:
    book = Book(
        id=uuid4(),
        **request.model_dump(),
    )

    try:
        books.create(book)
    except ExistsError as e:
        return ResourceExists(
            f"Book with ISBN<{book.isbn}> already exists.",
            book={"id": str(e.id)},
        )

    return ResourceCreated(book=book)


@books_api.get(
    "",
    status_code=200,
    response_model=Response[BookListEnvelope],
)
def read_all(books: BookRepositoryDependable) -> ResourceFound:
    return ResourceFound(books=list(books), count=len(books))


@books_api.get(
    "/{book_id}",
    status_code=200,
    response_model=Response[BookItemEnvelope],
)
def read_one(
    book_id: UUID,
    books: BookRepositoryDependable,
) -> ResourceFound | ResourceNotFound:
    try:
        return ResourceFound(book=books.read(book_id))
    except DoesNotExistError:
        pass

    return ResourceNotFound(f"Book with id<{book_id}> does not exist.")
