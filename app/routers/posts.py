from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Users, Posts
from app.schemas import PostCreate, PostOut
from app.utils.security import verify_token

router = APIRouter()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

oauth2 = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(
	token: str = Depends(oauth2), 
	db: Session = Depends(get_db)
	):
	payload = verify_token(token)

	if not payload:
		raise HTTPException(status_code=401, detail="Unauthorized")

	user = db.query(Users).filter(payload['sub'] == Users.username).first()

	if not user:
		raise HTTPException(status_code=401, detail="Forbidden")

	return user

@router.get('/', response_model=list[PostOut])
def get_all_posts(
	db: Session = Depends(get_db), 
	user: Users = Depends(get_current_user)
	):
	posts = db.query(Posts).filter(Posts.owner_id==user.id).all()
	return posts

@router.get('/{post_id}', response_model=PostOut)
def get_post(
	post_id: int, 
	user: Users = Depends(get_current_user), 
	db: Session = Depends(get_db)
	):
	post = db.query(Posts).filter(user.id == Posts.owner_id, post_id == Posts.id).first()

	if not post:
		raise HTTPException(status_code=404, detail="Post not Found")

	return post

@router.post('/', response_model=PostCreate)
def create_post(
	post: PostCreate, 
	user: Users = Depends(get_current_user), 
	db: Session = Depends(get_db)
	):
	new_post = Posts(title = post.title, content = post.content, owner_id = user.id)
	db.add(new_post)
	db.commit()
	db.refresh(new_post)
	return new_post

@router.delete('/{post_id}')
def delete_post(
	post_id: int, 
	user: Users = Depends(get_current_user), 
	db: Session = Depends(get_db)
	):
	post = db.query(Posts).filter(Posts.id == post_id, Posts.owner_id == user.id).first()
	if not post:
		raise HTTPException(status_code=404, detail="Post not found")
	db.delete(post)
	db.commit()

	return {'message': 'Post Deleted'}

@router.put('/{post_id}', response_model=PostCreate)
def update_post(
	post_id: int, 
	db_post: PostCreate, 
	user: Users = Depends(get_current_user), 
	db: Session = Depends(get_db)
	):

	post = db.query(Posts).filter(Posts.id == post_id, Posts.owner_id == user.id).first()

	if not post:
		raise HTTPException(status_code=404, detail="Post not found")

	post.title = db_post.title
	post.content = db_post.content

	db.commit()
	db.refresh(post)
	return post