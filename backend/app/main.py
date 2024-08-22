# main.py

from fastapi import FastAPI
from app.database import init_db
from app.routers import articles
from app.utils.scheduler import init_scheduler

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()  # Initialize the database
    init_scheduler()

app.include_router(articles.router)
