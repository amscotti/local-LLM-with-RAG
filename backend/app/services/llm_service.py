from app.db.database import get_db
from fastapi import HTTPException

def process_query(question: str, model: str, db) -> dict:
    # Здесь добавьте логику для обработки запроса к модели
    # Например, вызов модели и получение ответа
    # Верните ответ в виде словаря
    return {"answer": "Ваш ответ", "chunks": [], "files": []}

def initialize(model_name: str, embedding_model_name: str, documents_path: str, db) -> bool:
    # Логика инициализации модели
    return True
