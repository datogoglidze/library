from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Protocol
from uuid import UUID


class PublisherRepository(Protocol):  # pragma: no cover
    def create(self, publisher: Publisher) -> None:
        pass

    def read(self, publisher_id: UUID) -> Publisher:
        pass

    def __iter__(self) -> Iterator[Publisher]:
        pass

    def __len__(self) -> int:
        pass


@dataclass
class Publisher:
    id: UUID
    name: str
    country: str
