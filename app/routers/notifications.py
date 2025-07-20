from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Users, Notifications, Posts
from app.schemas import NotificationOut, NotificationCreate
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
		raise HTTPException(status_code=401, detail='Unauthorized')

	user = db.query(Users).filter(payload['sub'] == Users.username).first()

	if not user:
		raise HTTPException(status_code=401, detail='Forbidden')

	return user

@router.get('/', response_model=list[NotificationOut])
def get_notifications(db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
	notifications = db.query(Notifications).filter(user.id == Notifications.owner_id).all()
	return notifications

@router.get('/{notification_id}', response_model=NotificationOut)
def get_notification(notification_id: int, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
	notification = db.query(Notifications).filter(
		notification_id == Notifications.id, 
		user.id == Notifications.owner_id
		).first()

	if not notification:
		raise HTTPException(status_code=404, detail='Notification not found')

	return notification

@router.post('/{post_id}', response_model=NotificationOut)
def create_notification(post_id: int, db: Session = Depends(get_db)):
	post = db.query(Posts).filter(Posts.id == post_id).first()

	if not post:
		raise HTTPException(status_code=404, detail='Post not found')
	
	owner_id = post.owner_id
	new_notification = Notifications(content=f'New notification for {post.title}', owner_id=owner_id, post_id=post.id)
	db.add(new_notification)
	db.commit()
	db.refresh(new_notification)

	return new_notification