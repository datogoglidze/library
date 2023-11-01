from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Request
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


def get_author_repository(request: Request) -> list[dict[str, Any]]:
    return request.app.state.authors


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
def create_author(
    request: AuthorCreateRequest,
    authors: list[dict[str, Any]] = Depends(get_author_repository),
) -> JSONResponse | dict[str, Any]:
    author = {
        "id": uuid4(),
        "name": request.name,
        "birth_date": request.birth_date,
        "death_date": request.death_date,
        "bio": request.bio,
    }

    for author_info in authors:
        if author_info["name"] == author["name"]:
            return ResourceExists(
                f"Author with name<{author_info['name']}> already exists.",
                author={"id": str(author_info["id"])},
            )

    authors.append(author)

    return ResourceCreated(author=author)


@authors_api.get(
    "",
    status_code=200,
    response_model=Response[AuthorListEnvelope],
)
def read_all(
    authors: list[dict[str, Any]] = Depends(get_author_repository),
) -> ResourceFound:
    return ResourceFound(authors=authors, count=len(authors))


@authors_api.get(
    "/{author_id}",
    status_code=200,
    response_model=Response[AuthorItemEnvelope],
)
def read_one(
    author_id: UUID,
    authors: list[dict[str, Any]] = Depends(get_author_repository),
) -> ResourceFound | ResourceNotFound:
    for author_info in authors:
        if author_info["id"] == author_id:
            return ResourceFound(author=author_info)

    return ResourceNotFound(f"Author with id<{author_id}> does not exist.")
