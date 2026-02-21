from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import deps  
from src.db.repositories.game_repo import GameRepository
from src.services.logic import LogicService
from src.schemas.game import (
    GameStartResponse, 
    GameStepResponse, 
    GameAnswerRequest, 
    Question as QuestionSchema, 
    CharacterGuess
)

router = APIRouter()

@router.post("/start", response_model=GameStartResponse)
async def start_game(db: AsyncSession = Depends(deps.get_db)):
    repo = GameRepository(db)
    session = await repo.create_session()
    
    first_q_id = await LogicService.get_start_question_id(repo)
    q_data = await repo.get_question_by_id(first_q_id)
    
    return GameStartResponse(
        session_id=str(session.id),
        question=QuestionSchema(
            id=q_data.id,
            text=q_data.text,
            step=1,
            progression=0.0
        )
    )

@router.post("/answer", response_model=GameStepResponse)
async def process_answer(request: GameAnswerRequest, db: AsyncSession = Depends(deps.get_db)):
    repo = GameRepository(db)
    
    # 1. Сохраняем ответ пользователя
    answer_text = {1: "yes", 0: "no", 2: "dont_know"}.get(request.answer_id, "dont_know")
    await repo.save_answer(request.session_id, request.question_id, answer_text)
    
    # 2. Получаем историю и вызываем новый алгоритм
    history = await repo.get_session_history(request.session_id)
    decision = await LogicService.get_next_step(repo, history)
    
    # 3. Обработка решения алгоритма
    if decision['type'] == 'question':
        next_q = await repo.get_question_by_id(decision['question_id'])
        return GameStepResponse(
            type="question",
            payload=QuestionSchema(
                id=next_q.id,
                text=next_q.text,
                step=len(history) + 1,
                progression=0.0 # Можно будет добавить расчет прогресса позже
            )
        )
    else:
        # Алгоритм готов угадать персонажа
        char = await repo.get_character_by_id(decision['character_id'])
        return GameStepResponse(
            type="guess",
            payload=CharacterGuess(
                character_id=char.id,
                name=char.name,
                description=char.description or "Тайный персонаж",
                image_url="https://api.dicebear.com/7.x/bottts/svg", # Заглушка для фото
                confidence=decision['probability']
            )
        )