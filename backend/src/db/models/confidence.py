from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.db.session import Base

class Confidence(Base):
    __tablename__ = "confidence"

    id = Column(Integer, primary_key=True, index=True)
    
    character_id = Column(Integer, ForeignKey("characters.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    
    answer = Column(String, nullable=False) 
    
    confidence = Column(Float, default=1.0)

    character = relationship("Character")
    question = relationship("Question")