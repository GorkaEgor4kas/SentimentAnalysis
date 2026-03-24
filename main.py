from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from transformers import pipeline


from database import engine, get_db
from models import Base, SentimentAnalysis

#table creation
Base.metadata.create_all(bind=engine)


app = FastAPI()


class TextInput(BaseModel):
    text: str
    language: str = 'ru'

classifier = pipeline(
    "sentiment-analysis", 
    model="blanchefort/rubert-base-cased-sentiment",
)


class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    language: str
    timestamp: str
    id: int


@app.post("/analyze", response_model=SentimentResponse)
def analyze_text(request: TextInput, db: Session = Depends(get_db)):
    """
    Анализирует тональность текста и сохраняет результат в БД
    """

    label_map = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL", 
    "LABEL_2": "POSITIVE"
    }

    result = classifier(request.text)[0]
    sentiment = label_map.get(result['label'], result['label'])
    confidence = round(result['score'], 3)

    db_entry = SentimentAnalysis(
        text=request.text,
        sentiment=sentiment,
        confidence=confidence,
        language=request.language,
        timestamp=datetime.utcnow()
    )
    
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    return SentimentResponse(
        text = db_entry.text,
        sentiment = db_entry.sentiment,
        confidence=db_entry.confidence,
        language=db_entry.language,
        timestamp=db_entry.timestamp.isoformat(),
        id=db_entry.id
    )    

@app.get("/history")
def get_history(limit: int = 10, skip: int = 0, db: Session = Depends(get_db)):
    """
    Возвращает историю запросов из БД
    """
    entries = db.query(SentimentAnalysis)\
        .order_by(SentimentAnalysis.timestamp.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return [ 
        {
            "id": entry.id,
            "text": entry.text,
            "sentiment": entry.sentiment,
            "confidence": entry.confidence,
            "language": entry.language,
            "timestamp": entry.timestamp.isoformat()
        }

        for entry in entries

    ]

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """
    Возвращает статистику по запросам
    """
    total = db.query(SentimentAnalysis).count()

    from sqlalchemy import func
    sentiment_stats = db.query(
        SentimentAnalysis.sentiment,
        func.count(SentimentAnalysis.id)
    ).group_by(SentimentAnalysis.sentiment).all()

    return {
        "total_requests": total,
        "sentiment_distribution": dict(sentiment_stats),
        "last_request": db.query(SentimentAnalysis)\
            .order_by(SentimentAnalysis.timestamp.desc())\
            .first()\
            .timestamp.isoformat() if total > 0 else None
    }







