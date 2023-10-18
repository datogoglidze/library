from dataclasses import dataclass

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@dataclass
class Book(BaseModel):
    title: str
    author: str


shelf = []


@app.post("/books", status_code=201)
def create_book(book: Book) -> dict[str, str]:
    book_info = {
        "title": book.title,
        "author": book.author,
    }

    shelf.append(book_info)

    return book_info


@app.get("/books", status_code=200)
def show_shelf() -> dict[str, list[dict[str, str]]]:
    return {"shelf": shelf}
