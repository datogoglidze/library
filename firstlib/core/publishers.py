from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Protocol


class PublisherRepository(Protocol):  # pragma: no cover
    def create(self, publisher: Publisher) -> None:
        pass

    def read(self, publisher_id: str) -> Publisher:
        pass

    def __iter__(self) -> Iterator[Publisher]:
        pass

    def __len__(self) -> int:
        pass


@dataclass
class Publisher:
    id: str
    name: str
    country: str

    def __post_init__(self) -> None:
        self.name = self.name.lower()
