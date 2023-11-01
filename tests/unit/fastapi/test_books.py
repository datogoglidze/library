from unittest.mock import ANY

from firstlib.infra.fastapi.books import shelf
from tests.client import FirstlibApi
from tests.unit.fastapi.fake import Fake

fake = Fake()


def test_should_create(firstlib: FirstlibApi) -> None:
    book = fake.book()

    firstlib.books.create_one(
        from_data=book,
    ).assert_created(
        book={"id": ANY, **book},
    )


def test_should_not_duplicate(firstlib: FirstlibApi) -> None:
    book = firstlib.books.create_one(fake.book())

    firstlib.books.create_one(
        from_data=book.unpack(exclude=["id"]),
    ).assert_conflict(
        with_message=f"Book with ISBN<{book['isbn']}> already exists.",
        and_data={"book": {"id": book["id"]}},
    )


def test_should_list_all_created(firstlib: FirstlibApi) -> None:
    shelf.clear()

    fake_books = [
        firstlib.books.create_one(fake.book()).unpack(),
        firstlib.books.create_one(fake.book()).unpack(),
    ]

    firstlib.books.read_all().assert_ok(books=fake_books, count=len(fake_books))

    shelf.clear()


def test_should_read_one(firstlib: FirstlibApi) -> None:
    book = firstlib.books.create_one(fake.book())

    firstlib.books.read_one(with_id=book["id"]).assert_ok(book=book.unpack())


def test_should_not_list_anything_when_none_exists(firstlib: FirstlibApi) -> None:
    shelf.clear()

    firstlib.books.read_all().assert_ok(books=[], count=0)


def test_should_not_read_unknown(firstlib: FirstlibApi) -> None:
    unknown_book_id = fake.uuid()

    firstlib.books.read_one(
        with_id=unknown_book_id,
    ).assert_not_found(
        with_message=f"Book with id<{unknown_book_id}> does not exist.",
    )
