from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Users, Posts, Comments
from app.utils.security import verify_token
from app.schemas import CommentOut, CommentCreate

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl='/users/login')

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
	payload = verify_token(token)

	if not payload:
		raise HTTPException(status_code=401, detail="Unauthorized")

	user = db.query(Users).filter(payload['sub'] == Users.username).first()

	if not user:
		raise HTTPException(status_code=401, detail="Forbidden")

	return user

# Generally get comments.

@router.get('/{post_id}', response_model=list[CommentOut])
def get_all_comments(post_id: int, db: Session = Depends(get_db)):
	comments = db.query(Comments).filter(post_id == Comments.post_id).all()
	return comments

@router.get('/{user_id}', response_model=list[CommentOut])
def get_all_comments_of_user(user_id: int, db: Session = Depends(get_db)):
	user_comments = db.query(Comments).filter(Comments.owner_id == user_id).first()
	return user_comments

@router.get('/{comment_id}', response_model=CommentOut)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
	comment = db.query(Comments).filter(comment_id == Comments.id).first()

	if not comment:
		raise HTTPException(status_code=404, detail="Comment not found")

	return comment

