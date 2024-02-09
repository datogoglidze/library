from uuid import UUID, uuid4

from fastapi import APIRouter
from pydantic import BaseModel
from pydevtools.error import DoesNotExistError, ExistsError
from pydevtools.fastapi import (
    ResourceCreated,
    ResourceExists,
    ResourceFound,
    ResourceNotFound,
    Response,
)

from firstlib.core.authors import Author
from firstlib.infra.fastapi.dependable import AuthorRepositoryDependable

authors_api = APIRouter(tags=["Authors"])


class AuthorCreateRequest(BaseModel):
    name: str
    birth_date: str
    death_date: str
    bio: str


class AuthorItem(BaseModel):
    id: str
    name: str
    birth_date: str
    death_date: str
    bio: str


class AuthorItemEnvelope(BaseModel):
    author: AuthorItem


class AuthorListEnvelope(BaseModel):
    count: int
    authors: list[AuthorItem]


@authors_api.post(
    "",
    status_code=201,
    response_model=Response[AuthorItemEnvelope],
)
def create(
    request: AuthorCreateRequest,
    authors: AuthorRepositoryDependable,
) -> ResourceCreated | ResourceExists:
    author = Author(
        id=str(uuid4()),
        **request.model_dump(),
    )

    try:
        authors.create(author)
    except ExistsError as e:
        return ResourceExists(
            f"Author with name<{author.name}> already exists.",
            author={"id": str(e.id)},
        )

    return ResourceCreated(author=author)


@authors_api.get(
    "",
    status_code=200,
    response_model=Response[AuthorListEnvelope],
)
def read_all(authors: AuthorRepositoryDependable) -> ResourceFound:
    return ResourceFound(authors=list(authors), count=len(authors))


@authors_api.get(
    "/{author_id}",
    status_code=200,
    response_model=Response[AuthorItemEnvelope],
)
def read_one(
    author_id: str,
    authors: AuthorRepositoryDependable,
) -> ResourceFound | ResourceNotFound:
    try:
        return ResourceFound(author=authors.read(author_id))
    except DoesNotExistError:
        pass

    return ResourceNotFound(f"Author with id<{author_id}> does not exist.")
