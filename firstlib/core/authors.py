from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Protocol
from uuid import UUID


class AuthorRepository(Protocol):  # pragma: no cover
    def create(self, author: Author) -> None:
        pass

    def read(self, author_id: UUID) -> Author:
        pass

    def update(self, author: Author) -> None:
        pass

    def __iter__(self) -> Iterator[Author]:
        pass

    def __len__(self) -> int:
        pass


@dataclass
class Author:
    id: UUID
    name: str
    birth_date: str
    death_date: str
    bio: str

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, Author), f"Cannot compare to {type(other)}"

        return self.name == other.name
