from fastapi import Body, FastAPI

app = FastAPI()


books = [
	{
		"title": "Life of Pi",
		"author": "Yann Martel",
		"category": "Adventure",
	},
	{
		"title": "Star Wars",
		"author": "George Lucas",
		"category": "Science Fiction",
	},
	{
		"title": "Well, this is us",
		"author": "Stephen Chbosky",
		"category": "Biography",
	},
	{
		"title": "Last of Us",
		"author": "Neil Druckmann",
		"category": "Action",
	},
]


@app.get("/books")
async def read_all_books():
	return books


@app.get("/books/")
async def read_category_by_query(category: str):
	books_to_return = []
	for book in books:
		if book.get("category").casefold() == category.casefold():
			books_to_return.append(book)
	return books_to_return


# The order of arrangement is important
# Smaller endpoints should be at the beginning
@app.get("/books/byauthor/")
async def read_books_by_author(author: str):
	book_to_return = []
	for book in books:
		if book.get("author").casefold() == author.casefold():
			book_to_return.append(book)
	return book_to_return


@app.get("/books/{book_author}")
async def read_author_category_by_query(book_author: str, category: str):
	books_to_return = []
	for book in books:
		if (
			book.get("author").casefold() == book_author.casefold()
			and book.get("category").casefold() == category.casefold()
		):
			books_to_return.append(book)
	return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
	books.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
	for i in range(len(books)):
		if books[i].get("title").casefold() == updated_book.get("title").casefold():
			books[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title):
	for i in range(len(books)):
		if books[i].get("title").casefold() == book_title.casefold():
			books.pop(i)
			break
