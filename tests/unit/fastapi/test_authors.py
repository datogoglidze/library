from unittest.mock import ANY

import pytest
from pydevtools.http import Httpx
from pydevtools.testing import RestfulName, RestResource

from tests.unit.fastapi.fake import Fake

fake = Fake()


@pytest.fixture
def authors_api(http: Httpx) -> RestResource:
    return RestResource(http, RestfulName("author"))


def test_should_create(authors_api: RestResource) -> None:
    author = fake.author()

    (
        authors_api.create_one()
        .from_data(author)
        .ensure()
        .success()
        .with_code(201)
        .with_data(author={"id": ANY, **author})
    )


def test_should_not_duplicate(authors_api: RestResource) -> None:
    author = fake.author()
    authors_api.create_one().from_data(author).unpack()

    (
        authors_api.create_one()
        .from_data(author)
        .ensure()
        .fail()
        .with_code(409)
        .and_message(f"Author with name<{author['name']}> already exists.")
        .and_data(author={"id": ANY})
    )


def test_should_list_all_created(authors_api: RestResource) -> None:
    authors = [
        dict(authors_api.create_one().from_data(fake.author()).unpack()),
        dict(authors_api.create_one().from_data(fake.author()).unpack()),
    ]

    (
        authors_api.read_all()
        .ensure()
        .success()
        .with_code(200)
        .and_data(authors=authors, count=len(authors))
    )


def test_should_read_one(authors_api: RestResource) -> None:
    author = fake.author()
    id_ = authors_api.create_one().from_data(author).unpack().value_of("id").to(str)

    (
        authors_api.read_one()
        .with_id(id_)
        .ensure()
        .success()
        .with_code(200)
        .and_data(author={"id": id_, **author})
    )


def test_should_not_list_anything_when_none_exists(authors_api: RestResource) -> None:
    (
        authors_api.read_all()
        .ensure()
        .success()
        .with_code(200)
        .and_data(authors=[], count=0)
    )


def test_should_not_read_unknown(authors_api: RestResource) -> None:
    unknown_author_id = fake.uuid()

    (
        authors_api.read_one()
        .with_id(unknown_author_id)
        .ensure()
        .fail()
        .with_code(404)
        .and_message(f"Author with id<{unknown_author_id}> does not exist.")
    )
