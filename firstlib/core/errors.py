from dataclasses import dataclass
from uuid import UUID


@dataclass
class ExistsError(Exception):
    id: UUID | str


@dataclass
class DoesNotExistError(Exception):
    id: UUID | str
