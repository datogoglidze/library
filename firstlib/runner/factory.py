from __future__ import annotations

from pydevtools.repository import InMemoryRepository

from firstlib.core.authors import Author
from firstlib.core.book import Book
from firstlib.core.publishers import Publisher


class InMemoryInfraFactory:
    def authors(self) -> InMemoryRepository[Author]:
        return InMemoryRepository[Author]().with_unique(
            criteria=lambda item: f"name<{item.name}>"
        )

    def books(self) -> InMemoryRepository[Book]:
        return InMemoryRepository[Book]().with_unique(
            criteria=lambda item: f"isbn<{item.isbn}>"
        )

    def publishers(self) -> InMemoryRepository[Publisher]:
        return InMemoryRepository[Publisher]().with_unique(
            criteria=lambda item: f"name<{item.name}>"
        )
