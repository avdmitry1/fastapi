from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
	id: int
	title: str
	author: str
	description: str
	rating: int

	def __init__(self, id, title, author, description, rating):
		self.id = id
		self.title = title
		self.author = author
		self.description = description
		self.rating = rating


BOOKS = [
	Book(1, "Life of Pi", "Yann Martel", "A novel", 4),
	Book(2, "Star Wars", "George Lucas", "A science fiction novel", 5),
	Book(3, "Well, this is us", "Stephen Chbosky", "A biography", 3),
	Book(4, "Last of Us", "Neil Druckmann", "An action novel", 4),
	Book(5, "The Martian", "Andy Weir", "A science fiction novel", 4),
	Book(6, "The Hunger Games", "Suzanne Collins", "A dystopian novel", 4),
	Book(7, "The Da Vinci Code", "Dan Brown", "A thriller novel", 4),
	Book(8, "The Girl with the Dragon Tattoo", "Stieg Larsson", "A thriller novel", 4),
	Book(9, "The Da Vinci Code", "Dan Brown", "A thriller novel", 4),
	Book(10, "The Girl with the Dragon Tattoo", "Stieg Larsson", "A thriller novel", 4),
]


@app.get("/books")
async def read_all_books():
	return BOOKS


class BookRequest(BaseModel):
	id: int | None
	title: str = Field(min_length=3)
	author: str = Field(min_length=1)
	description: str = Field(min_length=1, max_length=25)
	rating: int = Field(gt=1, lt=10)


@app.post("/create-book")
async def create_book(book_request: BookRequest):
	new_book = Book(**book_request.model_dump())
	BOOKS.append(book_add(new_book))
	return new_book


def book_add(book: Book):
	book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
	return book
