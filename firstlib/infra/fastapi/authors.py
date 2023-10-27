from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from firstlib.infra.fastapi.docs import Response
from firstlib.infra.fastapi.response import (
    ResourceCreated,
    ResourceExists,
    ResourceFound,
    ResourceNotFound,
)

authors_api = APIRouter(tags=["Authors"])

all_authors: list[dict[str, Any]] = []


class AuthorCreateRequest(BaseModel):
    name: str
    birth_date: str
    death_date: str
    bio: str


class AuthorItem(BaseModel):
    id: UUID
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
def create_author(request: AuthorCreateRequest) -> JSONResponse | dict[str, Any]:
    author = {
        "id": uuid4(),
        "name": request.name,
        "birth_date": request.birth_date,
        "death_date": request.death_date,
        "bio": request.bio,
    }

    for author_info in all_authors:
        if author_info["name"] == author["name"]:
            return ResourceExists(
                f"Author with name<{author_info['name']}> already exists.",
                author={"id": str(author_info["id"])},
            )

    all_authors.append(author)

    return ResourceCreated(author=author)


@authors_api.get(
    "",
    status_code=200,
    response_model=Response[AuthorListEnvelope],
)
def read_all() -> ResourceFound:
    return ResourceFound(authors=all_authors, count=len(all_authors))


@authors_api.get(
    "/{author_id}",
    status_code=200,
    response_model=Response[AuthorItemEnvelope],
)
def read_one(author_id: UUID) -> ResourceFound | ResourceNotFound:
    for author_info in all_authors:
        if author_info["id"] == author_id:
            return ResourceFound(author=author_info)

    return ResourceNotFound(f"Author with id<{author_id}> does not exist.")
