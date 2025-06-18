from sqlalchemy import create_engine
from database import Base
from models_db import Quiz, Question, UserQuizAttempt, UserAnswer

# Настройки подключения к базе данных
DATABASE_URL = "mysql+mysqlconnector://root:123123@localhost:3306/db"

def migrate():
    """Создание таблиц для функционала тестирования и анкетирования"""
    engine = create_engine(DATABASE_URL)
    
    # Создаем таблицы
    Base.metadata.create_all(engine, tables=[
        Quiz.__table__,
        Question.__table__,
        UserQuizAttempt.__table__,
        UserAnswer.__table__
    ])
    
    print("Миграция успешно выполнена. Таблицы для тестов и анкет созданы.")

if __name__ == "__main__":
    migrate() 