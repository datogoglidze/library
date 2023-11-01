from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI

from firstlib.infra.fastapi.authors import authors_api
from firstlib.infra.fastapi.books import books_api
from firstlib.infra.fastapi.publishers import publishers_api

JsonDict = dict[str, Any]


@dataclass
class FastApiConfig:
    pass

    def setup(self) -> FastAPI:
        app = FastAPI()

        app.state.publishers = []
        app.state.authors = []

        app.include_router(books_api, prefix="/books")
        app.include_router(authors_api, prefix="/authors")
        app.include_router(publishers_api, prefix="/publishers")

        return app
