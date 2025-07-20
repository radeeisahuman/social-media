from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Users
from app.schemas import UserCreate, UserOut
from app.database import SessionLocal
from app.utils.security import hash_password, verify_password, generate_token

router = APIRouter()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@router.post('/register', response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
	if db.query(Users).filter(user.id == Users.id).first():
		raise HTTPException(status_code=400, detail="Username Taken")

	db_user = Users(username=user.username, password=hash_password(user.password))
	db.add(user)
	db.commit()
	db.refresh(db_user)
	return db_user

@router.post('/login')
def login_user(user: UserCreate, db: Session = Depends(get_db)):
	db_user = db.query(Users).filter(user.id == Users.id).first()
	if not db_user:
		raise HTTPException(status_code=400, detail="User Not Registered")

	if not verify_password(user.password, db_user.password):
		raise HTTPException(status_code=400, detail="Password did not match")

	token = generate_token({'sub': db_user.username})
	return {'access_token': token, 'token_type': 'bearer'}