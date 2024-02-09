from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from faker import Faker
from pydevtools.http import JsonObject


@dataclass
class Fake:
    faker: Faker = field(default_factory=Faker)

    def uuid(self) -> str:
        return str(self.faker.uuid4())

    def book(self, author_id: str, publisher_id: str) -> JsonObject[Any]:
        return JsonObject(
            {
                "name": self.uuid(),
                "author_id": author_id,
                "isbn": str(self.faker.isbn13()),
                "publisher_id": publisher_id,
                "total_pages": int(self.faker.random_digit_not_null()),
                "year": int(self.faker.year()),
            }
        )

    def author(self) -> JsonObject[Any]:
        return JsonObject(
            {
                "name": self.uuid(),
                "birth_date": self.uuid(),
                "death_date": self.uuid(),
                "bio": self.uuid(),
            }
        )

    def publisher(self) -> JsonObject[Any]:
        return JsonObject(
            {
                "name": self.uuid(),
                "country": self.uuid(),
            }
        )
