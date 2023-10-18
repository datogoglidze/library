from firstlib.book import create_book


def test_create_book():
    assert create_book("LOTR", "Tolkien") == "LOTR: Tolkien"
