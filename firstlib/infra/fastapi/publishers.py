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

from firstlib.core.publishers import Publisher
from firstlib.infra.fastapi.dependable import PublisherRepositoryDependable

publishers_api = APIRouter(tags=["Publishers"])


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
def create(
    request: PublisherCreateRequest,
    publishers: PublisherRepositoryDependable,
) -> ResourceCreated | ResourceExists:
    publisher = Publisher(
        id=uuid4(),
        **request.model_dump(),
    )

    try:
        publishers.create(publisher)
    except ExistsError as e:
        return ResourceExists(
            f"Publisher with name<{publisher.name}> already exists.",
            publisher={"id": str(e.id)},
        )

    return ResourceCreated(publisher=publisher)


@publishers_api.get(
    "",
    status_code=200,
    response_model=Response[PublisherListEnvelope],
)
def read_all(publishers: PublisherRepositoryDependable) -> ResourceFound:
    return ResourceFound(publishers=list(publishers), count=len(publishers))


@publishers_api.get(
    "/{publisher_id}",
    status_code=200,
    response_model=Response[PublisherItemEnvelope],
)
def read_one(
    publisher_id: UUID,
    publishers: PublisherRepositoryDependable,
) -> ResourceFound | ResourceNotFound:
    try:
        return ResourceFound(publisher=publishers.read(publisher_id))
    except DoesNotExistError:
        pass
    return ResourceNotFound(f"Publisher with id<{publisher_id}> does not exist.")
