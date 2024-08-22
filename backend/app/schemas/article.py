# schemas/article.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ArticleBase(BaseModel):
    title: str
    content: str
    author: Optional[str] = None
    date: datetime

class ArticleCreate(ArticleBase):
    pass

class ArticleSchema(ArticleBase):
    id: int

    class Config:
        orm_mode = True  # This allows Pydantic to work seamlessly with SQLAlchemy models
