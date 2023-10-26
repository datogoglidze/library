from unittest.mock import ANY

import pytest
from fastapi.testclient import TestClient

from firstlib.infra.fastapi import FastApiConfig
from tests.unit.client import RestfulName, RestResource
from tests.unit.fake import Fake

fake = Fake()
client = TestClient(FastApiConfig().setup())


@pytest.fixture
def authors() -> RestResource:
    return RestResource(TestClient(FastApiConfig().setup()), RestfulName("author"))


def test_should_create(authors: RestResource) -> None:
    author = fake.author()

    authors.create_one(
        from_data=author,
    ).assert_created(
        author={"id": ANY, **author},
    )
