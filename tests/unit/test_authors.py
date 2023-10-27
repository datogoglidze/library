from unittest.mock import ANY

import pytest
from fastapi.testclient import TestClient

from firstlib.infra.fastapi import FastApiConfig
from firstlib.infra.fastapi.authors import all_authors
from tests.unit.client import RestfulName, RestResource
from tests.unit.fake import Fake

fake = Fake()


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

    all_authors.clear()


def test_should_not_duplicate(authors: RestResource) -> None:
    author = authors.create_one(fake.author())

    authors.create_one(
        from_data=author.unpack(exclude=["id"]),
    ).assert_conflict(
        with_message=f"Author with name<{author['name']}> already exists.",
        and_data={"author": {"id": author["id"]}},
    )

    all_authors.clear()


def test_should_list_all_created(authors: RestResource) -> None:
    fake_authors = [
        authors.create_one(fake.author()).unpack(),
        authors.create_one(fake.author()).unpack(),
    ]

    authors.read_all().assert_ok(authors=fake_authors, count=len(fake_authors))

    all_authors.clear()


def test_should_read_one(authors: RestResource) -> None:
    author = authors.create_one(fake.author())

    authors.read_one(with_id=author["id"]).assert_ok(author=author.unpack())

    all_authors.clear()


def test_should_not_list_anything_when_none_exists(authors: RestResource) -> None:
    authors.read_all().assert_ok(authors=[], count=0)


def test_should_not_read_unknown(authors: RestResource) -> None:
    unknown_author_id = fake.uuid()

    authors.read_one(
        with_id=unknown_author_id,
    ).assert_not_found(
        with_message=f"Author with id<{unknown_author_id}> does not exist.",
    )
