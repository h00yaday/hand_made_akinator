from typing import List, Dict, Union
from src.db.repositories.game_repo import GameRepository
from src.core.algorithm import AkinatorLogic
class LogicService:
    @staticmethod
    async def _get_logic_instance(repo: GameRepository) -> AkinatorLogic:
        chars = await repo.get_all_characters()
        questions = await repo.get_all_questions()
        matrix = await repo.get_confidence_matrix()
        
        return AkinatorLogic(characters=chars, questions=questions, matrix=matrix)

    @staticmethod
    async def get_start_question_id(repo: GameRepository) -> int:
        logic = await LogicService._get_logic_instance(repo)
        return logic.get_start_question_id()

    @staticmethod
    async def get_next_step(repo: GameRepository, history: list) -> dict:
        logic = await LogicService._get_logic_instance(repo)
        return logic.get_next_step(user_history=history)