# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL pointing to the app folder
SQLALCHEMY_DATABASE_URL = "sqlite:///app/rnews.db"  # This saves the database in the app folder

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the ORM models
Base = declarative_base()

def init_db():
    # Import all models here to ensure they are registered with SQLAlchemy
    from app.models.article import Article  # Import your models here

    # Create the database tables
    Base.metadata.create_all(bind=engine)
