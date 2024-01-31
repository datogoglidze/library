from dataclasses import dataclass
from typing import Protocol

from fastapi import FastAPI

from firstlib.core.authors import AuthorRepository
from firstlib.core.book import BookRepository
from firstlib.core.publishers import PublisherRepository
from firstlib.infra.fastapi.authors import authors_api
from firstlib.infra.fastapi.books import books_api
from firstlib.infra.fastapi.publishers import publishers_api


class _InfraFactory(Protocol):  # pragma: no cover
    def authors(self) -> AuthorRepository:
        pass

    def books(self) -> BookRepository:
        pass

    def publishers(self) -> PublisherRepository:
        pass


@dataclass
class FastApiConfig:
    infra: _InfraFactory

    def setup(self) -> FastAPI:
        app = FastAPI()

        app.state.books = self.infra.books()
        app.state.authors = self.infra.authors()
        app.state.publishers = self.infra.publishers()

        app.include_router(books_api, prefix="/books")
        app.include_router(authors_api, prefix="/authors")
        app.include_router(publishers_api, prefix="/publishers")

        return app
