from firstlib.book import create_book


def test_create_book() -> None:
    assert create_book("LOTR", "Tolkien") == "LOTR: Tolkien"
