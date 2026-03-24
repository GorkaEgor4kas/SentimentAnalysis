from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from models import Base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/sentiment_db"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=True, bind=engine)


def get_db():
    db  = SessionLocal()
    try:
        yield db
    finally:
        db.close()

