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
        .and_data(author.with_a(id=ANY))
    )


def test_should_not_duplicate(authors_api: RestResource) -> None:
    author = authors_api.create_one().from_data(fake.author()).unpack()
    author_name = author.value_of("name").to(str)

    (
        authors_api.create_one()
        .from_data(author.drop("id"))
        .ensure()
        .fail()
        .with_code(409)
        .and_message(f"Author with name<{author_name}> already exists.")
        .and_data(author.select("id"))
    )


def test_should_list_all_created(authors_api: RestResource) -> None:
    authors = [
        authors_api.create_one().from_data(fake.author()).unpack(),
        authors_api.create_one().from_data(fake.author()).unpack(),
    ]

    authors_api.read_all().ensure().success().with_code(200).and_data(*authors)


def test_should_read_one(authors_api: RestResource) -> None:
    author = authors_api.create_one().from_data(fake.author()).unpack()

    (
        authors_api.read_one()
        .with_id(author.value_of("id").to(str))
        .ensure()
        .success()
        .with_code(200)
        .and_data(author)
    )


def test_should_not_list_anything_when_none_exists(authors_api: RestResource) -> None:
    authors_api.read_all().ensure().success().with_code(200).and_data()


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
