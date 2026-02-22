from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.db.session import Base

class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    
    status = Column(String, default="active")
    
    guessed_character_id = Column(Integer, ForeignKey("characters.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    guessed_character = relationship("Character")
    answers = relationship("GameAnswer", back_populates="session", cascade="all, delete-orphan")


class GameAnswer(Base):
    __tablename__ = "game_answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    
    answer = Column(String, nullable=False)

    session = relationship("GameSession", back_populates="answers")
    question = relationship("Question")