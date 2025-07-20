from fastapi import FastAPI
import app.models as models
from app.database import engine
from app.routers.auth import router as auth_router
from app.routers.post import router as post_router
from app.routers.comments import router as comment_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix='/users', tags=['Users'])
app.include_router(post_router, prefix='/posts', tags=['Posts'])
app.include_router(comment_router, prefix='comments', tags=['Comments'])