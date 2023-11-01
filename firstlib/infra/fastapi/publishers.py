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

publishers_api = APIRouter(tags=["Publishers"])


def get_publisher_repository(request: Request) -> Any:
    return request.app.state.publishers


class PublisherCreateRequest(BaseModel):
    name: str
    country: str


class PublisherItem(BaseModel):
    id: UUID
    name: str
    country: str


class PublisherItemEnvelope(BaseModel):
    publisher: PublisherItem


class PublisherListEnvelope(BaseModel):
    count: int
    publishers: list[PublisherItem]


@publishers_api.post(
    "",
    status_code=201,
    response_model=Response[PublisherItemEnvelope],
)
def create_publisher(
    request: PublisherCreateRequest,
    publishers: list[dict[str, Any]] = Depends(get_publisher_repository),
) -> JSONResponse | dict[str, Any]:
    publisher = {
        "id": uuid4(),
        "name": request.name,
        "country": request.country,
    }

    for publisher_info in publishers:
        if publisher_info["name"] == publisher["name"]:
            return ResourceExists(
                f"Publisher with name<{publisher_info['name']}> already exists.",
                publisher={"id": str(publisher_info["id"])},
            )

    publishers.append(publisher)

    return ResourceCreated(publisher=publisher)


@publishers_api.get(
    "",
    status_code=200,
    response_model=Response[PublisherListEnvelope],
)
def read_all(
    publishers: list[dict[str, Any]] = Depends(get_publisher_repository),
) -> ResourceFound:
    return ResourceFound(publishers=publishers, count=len(publishers))


@publishers_api.get(
    "/{publisher_id}",
    status_code=200,
    response_model=Response[PublisherItemEnvelope],
)
def read_one(
    publisher_id: UUID,
    publishers: list[dict[str, Any]] = Depends(get_publisher_repository),
) -> ResourceFound | ResourceNotFound:
    for publisher_info in publishers:
        if publisher_info["id"] == publisher_id:
            return ResourceFound(publisher=publisher_info)

    return ResourceNotFound(f"Publisher with id<{publisher_id}> does not exist.")
