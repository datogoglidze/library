from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

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

    def author(self) -> dict[str, Any]:
        return {
            "name": self.uuid(),
            "birth_date": self.uuid(),
            "death_date": self.uuid(),
            "bio": self.uuid(),
        }

    def publisher(self) -> dict[str, Any]:
        return {
            "name": self.uuid(),
            "country": self.uuid(),
        }
