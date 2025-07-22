from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Users, Follows
from app.schemas import FollowOut, FollowCreate
from app.utils.security import verify_token

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

@router.post('/{subscribed_id}', response_model=FollowOut)
def follow_user(
	subscribed_id: int, 
	follow: FollowCreate, 
	db: Session = Depends(get_db), 
	current_user: Users = Depends(get_current_user)
	):
	if not db.query(Users).filter(subscribed_id==Users.id).first():
		raise HTTPException(status_code=404, detail="The User you are trying to follow was not found")

	new_follow = Follows(subscriber_id=current_user.id, subscribed_id=subscribed_id)
	db.add(new_follow)
	db.commit()
	db.refresh(new_follow)
	return new_follow

@router.get('/', response_model=list[FollowOut])
def get_follows(db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
	follows_list = db.query(Follows).filter(user.id == subscriber_id).all()
	return follows_list

@router.get('/{subscribed_id}', response_model=FollowOut)
def get_followed_user(subscribed_id: int, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
	followed_user = db.query(Follows).filter(user.id == subscriber_id, subscribed_id=subscribed_id).first()

	if not followed_user:
		raise HTTPException(status_code=404, detail="Followed user not found")

	return followed_user