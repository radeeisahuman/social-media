from pydantic import BaseModel, Field
from typing import optional

class PostOut(BaseModel):
	id: int
	title: str = Field(..., max_length=100)
	content: optional[str] = ""
	comments: list

	class Config:
		orm_mode = True

class PostCreate(BaseModel):
	title: str = Field(..., max_length=100)
	content: optional[str] = ""

class CommentOut(BaseModel):
	id: int
	content: str

	class Config:
		orm_mode = True

class CommentCreate(BaseModel):
	content: str
	owner_id: int
	post_id: int

class UserOut(BaseModel):
	id: int
	username: str

	class Config:
		orm_mode = True

class UserCreate(BaseModel):
	username: str
	password: str
