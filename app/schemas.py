from pydantic import BaseModel, Field
from typing import optional

class PostOut(BaseModel):
	id: int
	title: str = Field(..., max_length=100)
	content: optional[str] = ""

	class Config:
		orm_mode = True

class PostCreate(BaseModel):
	title: str = Field(..., max_length=100)
	content: optional[str] = ""

class CommentOut(BaseModel):
	id: int
	content: str
	post_id: int
	owner_id: int

	class Config:
		orm_mode = True

class CommentCreate(BaseModel):
	content: str

class UserOut(BaseModel):
	id: int
	username: str

	class Config:
		orm_mode = True

class UserCreate(BaseModel):
	username: str
	password: str

class NotificationOut(BaseModel):
	id: int
	content: str
	owner_id: int
	post_id: int

	class Config:
		orm_mode = True

class NotificationCreate(BaseModel):
	content: str

class FollowOut(BaseModel):
	id: int
	subscriber_id : int
	subscribed_id: int

	class Config:
		orm_mode = True	

class FollowCreate(BaseModel):
	subscriber_id : int