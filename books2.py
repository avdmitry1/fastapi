from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
import uvicorn
from starlette import status

app = FastAPI()


class Book:
	id: int
	title: str
	author: str
	description: str
	rating: int
	published_date: int

	def __init__(self, id, title, author, description, rating, published_date):
		self.id = id
		self.title = title
		self.author = author
		self.description = description
		self.rating = rating
		self.published_date = published_date


BOOKS = [
	Book(1, "Life of Pi", "Yann Martel", "A novel", 4, 2011),
	Book(2, "Star Wars", "George Lucas", "A science fiction novel", 5, 2008),
	Book(3, "Well, this is us", "Stephen Chbosky", "A biography", 3, 2005),
	Book(4, "Last of Us", "Neil Druckmann", "An action novel", 4, 2020),
	Book(5, "The Martian", "Andy Weir", "A science fiction novel", 6, 2021),
	Book(6, "The Hunger Games", "Suzanne Collins", "A dystopian novel", 2, 2013),
	Book(7, "The Da Vinci Code", "Dan Brown", "A thriller novel", 7, 2017),
	Book(8, "The Girl with the Dragon Tattoo", "Stieg Larsson", "A thriller novel", 9, 2009),
	Book(9, "The Da Vinci Code", "Dan Brown", "A thriller novel", 1, 2011),
	Book(10, "The Girl with the Dragon Tattoo", "Stieg Larsson", "A thriller novel", 4, 2024),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
	return BOOKS


class BookRequest(BaseModel):
	id: Optional[int] = Field(description="Id is not needed to create", default=None)
	title: str = Field(min_length=3)
	author: str = Field(min_length=1)
	description: str = Field(min_length=1, max_length=25)
	rating: int = Field(gt=1, lt=10)
	published_date: int = Field(gt=2000, lt=2025)

	model_config = {
		"json_schema_extra": {
			"example": {
				"title": "new book",
				"author": "new author",
				"description": "tell about book",
				"rating": 5,
				"published_date": 2012,
			}
		}
	}


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
	new_book = Book(**book_request.model_dump())
	BOOKS.append(book_add(new_book))
	return new_book


def book_add(book: Book):
	book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
	return book


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0, lt=15)):
	for book in BOOKS:
		if book.id == book_id:
			return book
	return HTTPException(status_code=404, detail="Item not found")


@app.get("/books-filter-rating")
async def get_book_by_rating(books_rating: int = Query(gt=0, lt=15)):
	books_to_return = [book for book in BOOKS if book.id >= books_rating]
	return books_to_return


@app.put("/books-update", status_code=status.HTTP_204_NO_CONTENT)
async def books_update(book: BookRequest):
	book_changed = False
	for i in range(len(BOOKS)):
		if BOOKS[i].id == book.id:
			BOOKS[i] = book
			book_changed = True
	if not book_changed:
		return HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def book_delete(book_id: int = Path(gt=0, lt=15)):
	for i in range(len(BOOKS)):
		if BOOKS[i].id == book_id:
			BOOKS.pop(i)
			break


@app.get("/books_by_published_date")
async def book_published_date(published_date: int):
	books_to_return = [book for book in BOOKS if book.published_date >= published_date]
	return books_to_return


if __name__ == "__main__":
	uvicorn.run("books2:app", reload=True)
