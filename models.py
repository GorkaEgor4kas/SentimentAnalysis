from sqlalchemy import Integer, String, Text, DateTime, Float, Column
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    language = Column(String(10), default='ru')
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"ML_TEST(id = {self.id}, text = {self.text}, sentiment = {self.sentiment}, confidence = {self.confidence}, language = {self.language}, time = {self.timestamp})"
    