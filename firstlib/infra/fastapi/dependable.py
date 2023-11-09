from typing import Annotated

from fastapi import Depends
from starlette.requests import Request

from firstlib.core.authors import AuthorRepository
from firstlib.core.book import BookRepository
from firstlib.core.publishers import PublisherRepository


def get_books(request: Request) -> BookRepository:
    return request.app.state.books  # type: ignore


BookRepositoryDependable = Annotated[BookRepository, Depends(get_books)]


def get_authors(request: Request) -> AuthorRepository:
    return request.app.state.authors  # type: ignore


AuthorRepositoryDependable = Annotated[AuthorRepository, Depends(get_authors)]


def get_publishers(request: Request) -> PublisherRepository:
    return request.app.state.publishers  # type: ignore


PublisherRepositoryDependable = Annotated[PublisherRepository, Depends(get_publishers)]
