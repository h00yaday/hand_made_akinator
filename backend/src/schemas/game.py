from pydantic import BaseModel, HttpUrl
from typing import Optional, Union, Literal

class Question(BaseModel):
    id: int
    text: str
    step: int
    progression: Optional[float] = None

class CharacterGuess(BaseModel):
    character_id: int
    name: str
    description: str
    image_url: str
    confidence: float

class GameAnswerRequest(BaseModel):
    session_id: str
    answer_id: int

class GameFeedbackRequest(BaseModel):
    session_id: str
    success: bool
    character_name: Optional[str] = None

class GameStartResponse(BaseModel):
    session_id: str
    question: Question

class GameStepResponse(BaseModel):
    type: Literal["question", "guess"]
    payload: Union[Question, CharacterGuess]

class GameFeedbackResponse(BaseModel):
    status: str = "game_over"
    message: str = "Спасибо за игру! Мы стали умнее."