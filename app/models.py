from sqlalchemy import Column, ForeignKey, Integer, String, Text
from app.database import Base

class Posts(Base):
	__tablename__ = "posts"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True, nullable=False)
	content = Column(Text, nullable=False)
	owner_id = Column(Integer, ForeignKey('users.id'))
	owner = relationship("Users", back_populates="posts")
	comments = relationship("Comments", back_populates="belongs_to")

class Comments(Base):
	__tablename__ = "comments"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True, nullable=False)
	content = Column(Text, nullable=False)
	owner_id = Column(Integer, ForeignKey('users.id'))
	owner = relationship("Users", back_populates="comments")
	post_id = Column(Integer, ForeignKey('posts.id'))
	belongs_to = relationship("Comments", back_populates="comments")

class Users(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, index=True, nullable=False)
	password = Column(String, nullable=False)
	posts = relationship("Posts", back_populates="owner")
	comments = relationship("Comments", back_populates="owner")