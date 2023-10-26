from unittest.mock import ANY

import pytest
from fastapi.testclient import TestClient

from firstlib.infra.fastapi import FastApiConfig
from tests.unit.client import RestfulName, RestResource
from tests.unit.fake import Fake

fake = Fake()
client = TestClient(FastApiConfig().setup())


@pytest.fixture
def publishers() -> RestResource:
    return RestResource(TestClient(FastApiConfig().setup()), RestfulName("publisher"))


def test_should_create(publishers: RestResource) -> None:
    publisher = fake.publisher()

    publishers.create_one(
        from_data=publisher,
    ).assert_created(
        publisher={"id": ANY, **publisher},
    )
