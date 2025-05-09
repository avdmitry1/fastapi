from fastapi import FastAPI

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


@app.get("/books/{dynamic_param}")
async def read_all_books_by_param(dynamic_param: str):
    return {"dynamic_param": dynamic_param}
