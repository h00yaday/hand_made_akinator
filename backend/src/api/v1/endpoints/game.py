from fastapi import APIRouter
from src.schemas.game import (
    GameStartResponse, GameStepResponse, 
    GameAnswerRequest, GameFeedbackRequest, GameFeedbackResponse
)

router = APIRouter()

@router.post("/start", response_model=GameStartResponse)
async def start_game():
    return {
        "session_id": "550e8400-e29b-41d4-a716-446655440000",
        "question": {
            "id": 101,
            "text": "Ваш персонаж существует в реальности?",
            "step": 1
        }
    }

@router.post("/answer", response_model=GameStepResponse)
async def answer_question(data: GameAnswerRequest):
    if data.answer_id == 0:
        return {
            "type": "question",
            "payload": {
                "id": 204,
                "text": "Ваш персонаж мужчина?",
                "step": 2,
                "progression": 15.5
            }
        }
    return {
        "type": "guess",
        "payload": {
            "character_id": 55,
            "name": "Илон Маск",
            "description": "Инженер, предприниматель, миллиардер",
            "image_url": "https://path-to-image.jpg",
            "confidence": 85.0
        }
    }

@router.post("/feedback", response_model=GameFeedbackResponse)
async def game_feedback(data: GameFeedbackRequest):
    return {}