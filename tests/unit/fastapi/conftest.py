from pydevtools.repository import InMemoryRepository
from pytest import fixture
from starlette.testclient import TestClient

from firstlib.core.authors import Author
from firstlib.core.book import Book
from firstlib.core.publishers import Publisher
from firstlib.infra.fastapi import FastApiConfig


@fixture
def http() -> TestClient:
    return TestClient(
        FastApiConfig(
            books=InMemoryRepository[Book]().with_unique("isbn"),
            authors=InMemoryRepository[Author]().with_unique("name"),
            publishers=InMemoryRepository[Publisher]().with_unique("name"),
        ).setup()
    )
