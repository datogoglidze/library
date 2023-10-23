from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

api = APIRouter(tags=["Books"])

JsonDict = dict[str, Any]
shelf: list[JsonDict] = []


class BookCreateRequest(BaseModel):
    title: str
    author: str
    isbn: str
    publisher: str
    total_pages: int
    year: int


class BookCreateResponse(BaseModel):
    id: UUID
    title: str
    author: str
    isbn: str
    publisher: str
    total_pages: int
    year: int


@api.post(
    "",
    status_code=201,
    response_model=BookCreateResponse,
)
def create_book(request: BookCreateRequest) -> JsonDict:
    book_info = {
        "id": uuid4(),
        "title": request.title,
        "author": request.author,
        "isbn": request.isbn,
        "publisher": request.publisher,
        "total_pages": request.total_pages,
        "year": request.year,
    }

    for each_book in shelf:
        if each_book["isbn"] == book_info["isbn"]:
            raise HTTPException(status_code=409, detail="Book already exists")

    shelf.append(book_info)

    return book_info


@api.get("", status_code=200)
def show_shelf() -> list[JsonDict]:
    return shelf


@api.get("/{id}", status_code=200)
def show_one(id: UUID) -> JsonDict:
    for book_info in shelf:
        if book_info["id"] == id:
            return book_info
    raise HTTPException(status_code=404, detail="Book not found")
