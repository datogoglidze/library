from uuid import UUID, uuid4

from fastapi import APIRouter
from pydantic import BaseModel
from pydevtools.error import DoesNotExistError, ExistsError
from pydevtools.fastapi import (
    ResourceCreated,
    ResourceExists,
    ResourceFound,
    ResourceNotFound,
    Response,
)

from firstlib.core.book import Book
from firstlib.infra.fastapi.dependable import (
    AuthorRepositoryDependable,
    BookRepositoryDependable,
    PublisherRepositoryDependable,
)

books_api = APIRouter(tags=["Books"])


class BookCreateRequest(BaseModel):
    name: str
    author_id: UUID
    isbn: str
    publisher_id: UUID
    total_pages: int
    year: int


class BookItem(BaseModel):
    id: UUID
    name: str
    author_id: UUID
    isbn: str
    publisher_id: UUID
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
    authors: AuthorRepositoryDependable,
    publishers: PublisherRepositoryDependable,
    books: BookRepositoryDependable,
) -> ResourceCreated | ResourceExists | ResourceNotFound:
    try:
        authors.read(request.author_id)
    except DoesNotExistError as e:
        return ResourceNotFound(f"Author with id<{e.id}> does not exist.")

    try:
        publishers.read(request.publisher_id)
    except DoesNotExistError as e:
        return ResourceNotFound(f"Publisher with id<{e.id}> does not exist.")

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
    except DoesNotExistError as e:
        return ResourceNotFound(f"Book with id<{e.id}> does not exist.")
