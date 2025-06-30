from sqlalchemy import create_engine
from database import Base
from models_db import Feedback

# Настройки подключения к базе данных
DATABASE_URL = "mysql+mysqlconnector://root:123123@localhost:3306/db"

def migrate():
    """Создание таблиц для функционала тестирования и анкетирования"""
    engine = create_engine(DATABASE_URL)
    
    # Создаем таблицы
    Base.metadata.create_all(engine, tables=[
        Feedback.__table__,
    ])
    
    print("Миграция успешно выполнена. Таблицы для тестов и анкет созданы.")

if __name__ == "__main__":
    migrate() 