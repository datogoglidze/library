from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from unittest.mock import MagicMock
from uuid import UUID, uuid4

from faker import Faker


@dataclass
class Fake:
    faker: Faker = field(default_factory=Faker)

    def uuid(self) -> str:
        return str(self.faker.uuid4())

    def book(self) -> dict[str, Any]:
        return {
            "title": str(self.faker.job()),
            "author": str(self.faker.first_name()),
            "isbn": str(self.faker.isbn13()),
            "publisher": str(self.faker.company()),
            "total_pages": int(self.faker.random_digit_not_null()),
            "year": int(self.faker.year()),
        }


@dataclass
class FakeBook:
    id: UUID = field(default_factory=uuid4)
    author: str = field(default_factory=uuid4)
    isbn: str = field(default_factory=uuid4)
    publisher: str = field(default_factory=uuid4)
    total_pages: int = field(default_factory=uuid4)
    year: int = field(default_factory=lambda: 0)

    def create_request(self) -> dict[str, Any]:
        return {
            "author": self.author,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "total_pages": self.total_pages,
            "year": self.year,
        }

    def as_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "author": self.author,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "total_pages": self.total_pages,
            "year": self.year,
        }
