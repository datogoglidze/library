from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Protocol


class AuthorRepository(Protocol):  # pragma: no cover
    def create(self, author: Author) -> None:
        pass

    def read(self, author_id: str) -> Author:
        pass

    def __iter__(self) -> Iterator[Author]:
        pass

    def __len__(self) -> int:
        pass


@dataclass
class Author:
    id: str
    name: str
    birth_date: str
    death_date: str
    bio: str

    def __post_init__(self) -> None:
        self.name = self.name.lower()
