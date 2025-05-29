from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path, status
from pydantic import BaseModel, Field
import uvicorn
from models import Todos
from database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter(tags=["Todo"])


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
	title: str = Field(min_length=3)
	desc: str = Field(min_length=3, max_length=100)
	priority: int = Field(gt=0, lt=6)
	complete: bool


@router.get("/")
async def read_all(db: db_dependency):
	return db.query(Todos).all()


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
	todo = db.query(Todos).filter(Todos.id == todo_id).first()
	if todo is None:
		raise HTTPException(status_code=404, detail="Todo not found")
	return todo


@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
	todo_model = Todos(**todo_request.model_dump())
	db.add(todo_model)
	db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
	todo_model = db.query(Todos).filter(Todos.id == todo_id).filter()
	if todo_model is None:
		raise HTTPException(status_code=404, detail="Todo not found")

	todo_model.title = todo_request.title
	todo_model.desc = todo_request.desc
	todo_model.priority = todo_request.priority
	todo_model.complete = todo_request.complete
	db.add(todo_model)
	db.commit()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
	todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
	if todo_model is None:
		raise HTTPException(status_code=404, detail="todos not found")

	db.delete(todo_model)
	db.commit()


if __name__ == "__main__":
	uvicorn.run("main:app", reload=True)
