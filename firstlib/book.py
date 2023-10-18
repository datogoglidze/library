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
def create_book(book: Book):
    book = {
        "title": book.title,
        "author": book.author,
    }

    shelf.append(book)

    return book


@app.get("/books", status_code=200)
def show_shelf():
    return {"shelf": shelf}
