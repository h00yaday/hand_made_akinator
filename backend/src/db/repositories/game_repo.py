from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.db.models.game_session import GameSession, GameAnswer
from src.db.models.question import Question
from src.db.models.character import Character

class GameRepository:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def create_session(self) -> GameSession:
        """
        Создает новую игровую сессию со статусом 'active'.
        """
        new_session = GameSession(status="active")
        self.db.add(new_session)
        await self.db.commit()
        await self.db.refresh(new_session)
        return new_session

    async def get_question_by_id(self, q_id: int) -> Question:
        """
        Получает текст и категорию вопроса по его ID.
        """
        result = await self.db.execute(select(Question).where(Question.id == q_id))
        return result.scalar_one_or_none()

    async def save_answer(self, session_id: str, question_id: int, answer_text: str):
        """
        Сохраняет ответ пользователя в таблицу истории ответов (game_answers).
        """
        new_answer = GameAnswer(
            session_id=int(session_id), # Конвертируем из str в int для БД
            question_id=question_id,
            answer=answer_text
        )
        self.db.add(new_answer)
        await self.db.commit()

    async def get_session_history(self, session_id: str):
        """
        Вытягивает все предыдущие ответы сессии. 
        Этот список мы будем передавать аналитику в функцию calculate_next_step.
        """
        result = await self.db.execute(
            select(GameSession)
            .where(GameSession.id == int(session_id))
            .options(selectinload(GameSession.answers))
        )
        session = result.scalar_one_or_none()
        if not session:
            return []
        
        # Формируем список словарей, который ожидает LogicService
        return [
            {"question_id": a.question_id, "answer": a.answer} 
            for a in session.answers
        ]

    async def get_character_by_id(self, char_id: int) -> Character:
        """
        Получает данные персонажа (имя, описание), когда алгоритм готов сделать догадку.
        """
        result = await self.db.execute(select(Character).where(Character.id == char_id))
        return result.scalar_one_or_none()