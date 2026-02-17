from typing import List, Dict, Union

# Попытка импорта из ветки аналитика. 
# Когда она создаст папку 'logic' и файл 'engine.py', импорт заработает автоматически.
try:
    from src.logic.engine import get_initial_question, calculate_next_step
except ImportError:
    # --- ВРЕМЕННЫЕ ЗАГЛУШКИ (пока аналитик не закончила работу) ---
    def get_initial_question() -> int:
        # Начинаем с первого вопроса из сида: "Реальный человек?" [cite: 8]
        return 1 

    def calculate_next_step(history: List[Dict], threshold: float = 0.8) -> Dict:
        """
        Простая логика для тестов: выдает вопросы по порядку (1 -> 2 -> 3...).
        Если вопросы кончились, выдает 'угаданного' персонажа.
        """
        asked_ids = [item['question_id'] for item in history]
        
        # У нас в сиде 5 вопросов [cite: 8]
        next_id = 1
        while next_id in asked_ids and next_id <= 5:
            next_id += 1
            
        if next_id > 5:
            # Если все вопросы заданы, просто выдаем Гарри Поттера (ID 1) для теста [cite: 6]
            return {
                "status": "guess", 
                "character_id": 1, 
                "probability": 0.95
            }
        
        return {
            "status": "question", 
            "question_id": next_id
        }

# --- ОСНОВНОЙ СЕРВИС ---

class LogicService:
    @staticmethod
    def get_start_question_id() -> int:
        """
        Возвращает ID самого первого вопроса для новой игры.
        """
        return get_initial_question()

    @staticmethod
    def get_next_step(history: List[Dict], threshold: float = 0.8) -> Dict:
        """
        Принимает историю ответов и решает: задать новый вопрос или угадать персонажа.
        history формат: [{'question_id': 1, 'answer': 'yes'}, ...]
        """
        # Здесь происходит магия аналитика (энтропия, вероятности и т.д.)
        result = calculate_next_step(history, threshold)
        return result