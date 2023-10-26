from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from firstlib.infra.fastapi.docs import Response
from firstlib.infra.fastapi.response import ResourceCreated

authors_api = APIRouter(tags=["Authors"])

authors: list[dict[str, Any]] = []


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


@authors_api.post(
    "",
    status_code=201,
    response_model=Response[AuthorItemEnvelope],
)
def create_author(request: AuthorCreateRequest) -> ResourceCreated:
    author = {
        "id": uuid4(),
        "name": request.name,
        "birth_date": request.birth_date,
        "death_date": request.death_date,
        "bio": request.bio,
    }

    for each_author in authors:
        if each_author["name"] == author["name"]:
            raise HTTPException(status_code=409, detail="Author already exists")

    authors.append(author)

    return ResourceCreated(author=author)
