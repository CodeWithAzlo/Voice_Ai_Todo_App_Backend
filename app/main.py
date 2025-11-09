from fastapi import FastAPI
from .database import Base, engine
from .routes import todo

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Voice Todo AI Created By codewithazlo")

app.include_router(todo.router)

