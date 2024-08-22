# routers/articles.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.article import Article
from app.schemas.article import ArticleSchema, ArticleCreate
from app.database import SessionLocal
from app.services.data_acquisition import DataAcquisition
from dotenv import load_dotenv
import os

router = APIRouter()
load_dotenv()  # Load environment variables

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/fetch-now/")
async def fetch_now(db: Session = Depends(get_db)):
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not found.")
    
    # print(f"Using API Key: {api_key}")  # Debugging line
    
    search_terms = ["Ruto"]

    acquisition = DataAcquisition(api_key, search_terms)
    acquisition.fetch_and_save_articles(db)
    return {"status": "fetching completed"}

# Other routes remain unchanged

@router.get("/articles/", response_model=List[ArticleSchema])
async def read_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    articles = db.query(Article).offset(skip).limit(limit).all()
    return articles

@router.get("/articles/{article_id}", response_model=ArticleSchema)
async def read_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post("/articles/", response_model=ArticleSchema)
async def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(title=article.title, content=article.content, author=article.author, date=article.date)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@router.delete("/articles/{article_id}", response_model=ArticleSchema)
async def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(article)
    db.commit()
    return article

@router.get("/articles/search/", response_model=List[ArticleSchema])
async def search_articles(term: str, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(Article.content.contains(term)).all()
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found with the given term")
    return articles