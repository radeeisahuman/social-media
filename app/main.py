from fastapi import FastAPI
import app.models as models
from app.database import engine
from app.routers.auth import router as auth_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix='/users', tags=['Users'])