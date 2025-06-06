from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Настройки подключения
DATABASE_URL = "mysql+mysqlconnector://<username>:<password>@localhost:3306/<database_name>"

# Создание движка базы данных
engine = create_engine(DATABASE_URL)

# Проверка подключения
try:
    with engine.connect() as connection:
        print("Подключение к базе данных успешно!")
except SQLAlchemyError as e:
    print(f"Ошибка подключения: {e}")

# Создание базового класса для моделей
Base = declarative_base()

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
