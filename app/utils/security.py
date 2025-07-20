from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException
from datetime import datetime, timedelta

SECRET_KEY = '123456'
ALGORITHM = "HS256"
TOKEN_EXPIRES = timedelta(minutes=30)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash_password(plain):
	return pwd_context.hash(plain)

def verify_password(plain, hashed):
	return pwd_context.verify(plain, hashed)

def generate_token(data: dict, expires_delta: timedelta = None):
	to_encode = data.copy()
	expire = datetime.utcnow() + (expires_delta or TOKEN_EXPIRES)
	to_encode.update({'exp': expire})
	return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
	try:
		return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
	except:
		raise HTTPException(status_code=401, detail="Invalid Token")