import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from models_db import Base
from database import engine

def wait_for_db():
    """Ожидание доступности базы данных"""
    max_retries = 30
    retry_interval = 2
    
    for i in range(max_retries):
        try:
            # Пробуем подключиться к базе данных
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                print("Подключение к базе данных успешно!")
                return True
        except OperationalError as e:
            print(f"Попытка {i+1}/{max_retries}: Ожидание базы данных... ({e})")
            time.sleep(retry_interval)
    
    print("Не удалось подключиться к базе данных после нескольких попыток")
    return False

def init_db():
    """Инициализация базы данных"""
    print("Начало инициализации базы данных...")
    
    # Ожидание доступности базы данных
    if not wait_for_db():
        return False
    
    try:
        # Создание всех таблиц
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно созданы")
        
        # Здесь можно добавить начальные данные, если нужно
        # Например, создание пользователя admin, отделов и т.д.
        
        return True
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        return False

if __name__ == "__main__":
    success = init_db()
    if success:
        print("Инициализация базы данных завершена успешно")
    else:
        print("Инициализация базы данных завершилась с ошибками") 