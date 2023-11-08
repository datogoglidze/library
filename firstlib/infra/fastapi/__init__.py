from dataclasses import dataclass

from fastapi import FastAPI

from firstlib.core.authors import AuthorRepository
from firstlib.core.book import BookRepository
from firstlib.core.publishers import PublisherRepository
from firstlib.infra.fastapi.authors import authors_api
from firstlib.infra.fastapi.books import books_api
from firstlib.infra.fastapi.publishers import publishers_api


@dataclass
class FastApiConfig:
    books: BookRepository
    authors: AuthorRepository
    publishers: PublisherRepository

    def setup(self) -> FastAPI:
        app = FastAPI()

        app.state.books = self.books
        app.state.authors = self.authors
        app.state.publishers = self.publishers

        app.include_router(books_api, prefix="/books")
        app.include_router(authors_api, prefix="/authors")
        app.include_router(publishers_api, prefix="/publishers")

        return app
