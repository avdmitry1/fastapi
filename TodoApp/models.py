from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Users(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	email = Column(String, unique=True, nullable=False)
	username = Column(String, nullable=False)
	first_name = Column(String)
	last_name = Column(String, nullable=False)
	hashed_password = Column(String, nullable=False)
	is_active = Column(Boolean, default=True)
	role = Column(String, nullable=False)

	todos = relationship("Todos", back_populates="owner")


class Todos(Base):
	__tablename__ = "todos"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, nullable=False)
	desc = Column(String, nullable=False)
	priority = Column(Integer, nullable=False)
	complete = Column(Boolean, default=False)
	owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

	owner = relationship("Users", back_populates="todos")
