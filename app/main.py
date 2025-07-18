from fastapi import FastAPI
import app.models as models
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()