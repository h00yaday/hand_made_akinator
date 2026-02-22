from sqlalchemy import Column, Integer, String
from src.db.session import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String)       
    gender = Column(String)         
    description = Column(String)    
    status = Column(String, default="verified") 