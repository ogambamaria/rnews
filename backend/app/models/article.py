# models/articles.py

from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from app.database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    url = Column(String, index=True)
    summary = Column(Text, nullable=True)
    category = Column(String, index=True, nullable=True)
    sentiment = Column(Float, nullable=True)
    date = Column(DateTime)
