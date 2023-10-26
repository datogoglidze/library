from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from firstlib.infra.fastapi.docs import Response
from firstlib.infra.fastapi.response import ResourceCreated

publishers_api = APIRouter(tags=["Publishers"])

publishers: list[dict[str, Any]] = []


class PublisherCreateRequest(BaseModel):
    name: str
    country: str


class PublisherItem(BaseModel):
    id: UUID
    name: str
    country: str


class PublisherItemEnvelope(BaseModel):
    publisher: PublisherItem


@publishers_api.post(
    "",
    status_code=201,
    response_model=Response[PublisherItemEnvelope],
)
def create_publisher(request: PublisherCreateRequest) -> ResourceCreated:
    publisher_info = {
        "id": uuid4(),
        "name": request.name,
        "country": request.country,
    }

    for each_publisher in publishers:
        if each_publisher["name"] == publisher_info["name"]:
            raise HTTPException(status_code=409, detail="Publisher already exists")

    publishers.append(publisher_info)

    return ResourceCreated(publisher=publisher_info)
