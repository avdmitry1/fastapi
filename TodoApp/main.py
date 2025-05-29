from fastapi import FastAPI
import uvicorn
from models import Base
from database import engine
from routers import auth, todos

app = FastAPI()
app.include_router(auth.router_auth)
app.include_router(todos.router_todos)

Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
	uvicorn.run("main:app", reload=True)
