from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Protocol
from uuid import UUID


class BookRepository(Protocol):  # pragma: no cover
    def create(self, book: Book) -> None:
        pass

    def read(self, book_id: UUID) -> Book:
        pass

    def __iter__(self) -> Iterator[Book]:
        pass

    def __len__(self) -> int:
        pass


@dataclass
class Book:
    id: str
    name: str
    author_id: str
    isbn: str
    publisher_id: str
    total_pages: int
    year: int

    def __post_init__(self) -> None:
        self.isbn = self.isbn.lower()
