from fastapi import FastAPI
import app.models
from app.database import engine

app.models.Base.metadata.create_all(bind=engine)

app = FastAPI()