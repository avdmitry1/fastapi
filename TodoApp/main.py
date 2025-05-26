from fastapi import FastAPI
import uvicorn
import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
	uvicorn.run("main:app", reload=True)
