import pydantic
from database import Base
from sqlalchemy import Boolean, Column, Integer, String


class Todos(Base):
	__tablename__ = "todos"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String)
	desc = Column(String)
	priority = Column(Integer)
	complete = Column(Boolean, default=False)
