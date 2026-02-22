import asyncio
import sys
import os

# Добавляем текущую папку в путь, чтобы видеть папку src
sys.path.append(os.getcwd())

from sqlalchemy import text
from src.db.session import async_session_maker
from src.db.models import Character, Question, Confidence

# --- ДАННЫЕ ОТ АНАЛИТИКА ---

# 1. Персонажи
CHARACTERS_DATA = [
    {"name": 'Harry Potter',      "category": 'book',        "gender": 'male'},
    {"name": 'Hermione Granger',  "category": 'book',        "female": 'female'}, # Исправим поле gender в логике
    {"name": 'Tony Stark',        "category": 'movie',       "gender": 'male'},
    {"name": 'Elon Musk',         "category": 'real_person', "gender": 'male'},
    {"name": 'Taylor Swift',      "category": 'real_person', "gender": 'female'},
    {"name": 'Pikachu',           "category": 'anime',       "gender": 'other'},
    {"name": 'Darth Vader',       "category": 'movie',       "gender": 'male'},
    {"name": 'Elsa',              "category": 'cartoon',     "gender": 'female'},
    {"name": 'Sherlock Holmes',   "category": 'book',        "gender": 'male'},
    {"name": 'Cristiano Ronaldo', "category": 'real_person', "gender": 'male'},
]

# 2. Вопросы
QUESTIONS_DATA = [
    {"text": 'Реальный человек?',         "category": 'origin'},     # index 0
    {"text": 'Волшебник или волшебница?', "category": 'occupation'}, # index 1
    {"text": 'Мужской персонаж?',         "category": 'gender'},     # index 2
    {"text": 'Из книги или фильма?',      "category": 'origin'},     # index 3
    {"text": 'Носит маску или костюм?',   "category": 'appearance'}, # index 4
]

# 3. Ответы (Матрица связей)
# Формат: [Question_0, Question_1, Question_2, Question_3, Question_4]
# 0 = "no", 4 = "yes", 2 = "dont_know"
ANSWERS_MATRIX = [
    [0, 4, 4, 4, 0], # Harry Potter
    [0, 4, 0, 4, 0], # Hermione (Gender "no" means Female here based on context)
    [0, 0, 4, 4, 4], # Tony Stark
    [4, 0, 4, 0, 0], # Elon Musk
    [4, 0, 0, 0, 0], # Taylor Swift
    [0, 0, 2, 0, 0], # Pikachu (Gender "2" -> dont_know/other)
    [0, 0, 4, 4, 4], # Darth Vader
    [0, 4, 0, 0, 0], # Elsa
    [0, 0, 4, 4, 0], # Sherlock Holmes
    [4, 0, 4, 0, 0], # Cristiano Ronaldo
]

def map_score_to_answer(score: int) -> str:
    """Переводит число аналитика в строковый ответ для БД"""
    if score == 4:
        return "yes"
    elif score == 0:
        return "no"
    return "dont_know"

async def seed_database():
    async with async_session_maker() as session:
        print("🌱 Начинаем посев данных...")

        # 1. Очистка старых данных (опционально, чтобы не дублировать)
        print("   Очистка таблиц...")
        await session.execute(text("TRUNCATE TABLE confidence, characters, questions RESTART IDENTITY CASCADE"))
        
        # 2. Добавляем вопросы
        print("   Добавление вопросов...")
        questions_db = []
        for q_data in QUESTIONS_DATA:
            q = Question(text=q_data["text"], category=q_data["category"])
            session.add(q)
            questions_db.append(q)
        await session.flush() # Чтобы получить ID вопросов

        # 3. Добавляем персонажей и связи (Ответы)
        print("   Добавление персонажей и связей...")
        for char_idx, char_data in enumerate(CHARACTERS_DATA):
            # Исправляем возможные неточности в ключах (в данных аналитика было female вместо gender для Гермионы)
            gender = char_data.get("gender") or char_data.get("female", "unknown")
            
            character = Character(
                name=char_data["name"],
                category=char_data["category"],
                gender=gender,
                status="verified"
            )
            session.add(character)
            await session.flush() # Получаем ID персонажа

            # Создаем связи (Confidence) для этого персонажа
            char_answers = ANSWERS_MATRIX[char_idx]
            
            for q_idx, score in enumerate(char_answers):
                answer_str = map_score_to_answer(score)
                question = questions_db[q_idx]

                confidence_entry = Confidence(
                    character_id=character.id,
                    question_id=question.id,
                    answer=answer_str,
                    confidence=1.0 # Аналитик уверен на 100%
                )
                session.add(confidence_entry)

        await session.commit()
        print("✅ База данных успешно заполнена!")

if __name__ == "__main__":
    asyncio.run(seed_database())