from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import deps  # Используем твои зависимости
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
    
    # 1. Создаем сессию
    session = await repo.create_session()
    
    # 2. Получаем первый вопрос через LogicService
    first_q_id = LogicService.get_start_question_id()
    question_data = await repo.get_question_by_id(first_q_id)
    
    if not question_data:
        raise HTTPException(status_code=404, detail="Вопросы не найдены в базе")

    return GameStartResponse(
        session_id=str(session.id),
        question=QuestionSchema(
            id=question_data.id,
            text=question_data.text,
            step=1,
            progression=0.0
        )
    )

@router.post("/answer", response_model=GameStepResponse)
async def process_answer(request: GameAnswerRequest, db: AsyncSession = Depends(deps.get_db)):
    repo = GameRepository(db)
    
    # Маппинг: 1: yes, 0: no, 2: dont_know
    answer_map = {1: "yes", 0: "no", 2: "dont_know"}
    answer_text = answer_map.get(request.answer_id, "dont_know")

    # 1. Сохраняем ответ в базу
    await repo.save_answer(request.session_id, request.question_id, answer_text)
    
    # 2. Берем историю и идем к аналитику (через LogicService)
    history = await repo.get_session_history(request.session_id)
    decision = LogicService.get_next_step(history)
    
    # 3. Формируем ответ согласно твоей схеме GameStepResponse
    if decision["status"] == "question":
        next_q = await repo.get_question_by_id(decision["question_id"])
        return GameStepResponse(
            type="question",
            payload=QuestionSchema(
                id=next_q.id,
                text=next_q.text,
                step=len(history) + 1,
                progression=len(history) * 10.0 # Временный прогресс
            )
        )
    else:
        char = await repo.get_character_by_id(decision["character_id"])
        return GameStepResponse(
            type="guess",
            payload=CharacterGuess(
                character_id=char.id,
                name=char.name,
                description=char.description or "",
                image_url="https://api.dicebear.com/7.x/bottts/svg", 
                confidence=decision.get("probability", 0.9)
            )
        )