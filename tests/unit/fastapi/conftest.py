from pytest import fixture
from starlette.testclient import TestClient

from firstlib.core.authors import Author
from firstlib.core.book import Book
from firstlib.core.publishers import Publisher
from firstlib.infra.fastapi import FastApiConfig
from firstlib.infra.in_memory import InMemoryRepository


@fixture
def http() -> TestClient:
    return TestClient(
        FastApiConfig(
            books=InMemoryRepository[Book](),
            authors=InMemoryRepository[Author](),
            publishers=InMemoryRepository[Publisher](),
        ).setup()
    )
