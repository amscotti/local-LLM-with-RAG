from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, JSON
from passlib.context import CryptContext
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer)
    department_id = Column(Integer)
    access_id = Column(Integer)
    auth_key = Column(String(255), nullable=True)  # Ключ аутентификации
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def check_password(self, password: str) -> bool:
        """Проверка правильности пароля."""
        return pwd_context.verify(password, self.password)

class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(255), nullable=False)

class Access(Base):
    __tablename__ = "access"

    id = Column(Integer, primary_key=True, index=True)
    access_name = Column(String(50), unique=True, nullable=False)  # Название уровня доступа

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # Название контента
    description = Column(Text, nullable=True)  # Описание контента
    file_path = Column(String(255), nullable=False)  # Путь к файлу
    access_level = Column(Integer, ForeignKey("access.id"), nullable=False)  # Уровень доступа
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)  # ID отдела
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=True)  # ID тега

    access = relationship("Access")  # Связь с таблицей Access
    department = relationship("Department")  # Связь с таблицей Department
    tag = relationship("Tag")  # Связь с таблицей Tag

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String(255), nullable=False)  # Название тега

class ContentBase(BaseModel):
    id: int
    title: str
    description: str
    file_path: str

    class Config:
        orm_mode = True

# Модели для системы тестирования и анкетирования
class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # Название теста/анкеты
    description = Column(Text, nullable=True)  # Описание теста/анкеты
    is_test = Column(Boolean, default=False)  # True - тест (с правильными ответами), False - анкета
    department_id = Column(Integer, ForeignKey("department.id"), nullable=True)  # ID отдела (если тест для конкретного отдела)
    access_level = Column(Integer, ForeignKey("access.id"), nullable=True)  # Уровень доступа
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    department = relationship("Department")  # Связь с таблицей Department
    access = relationship("Access")  # Связь с таблицей Access
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    text = Column(Text, nullable=False)  # Текст вопроса
    question_type = Column(String(20), nullable=False)  # Тип вопроса: single_choice, multiple_choice, text
    options = Column(JSON, nullable=True)  # Варианты ответов в формате JSON
    correct_answer = Column(JSON, nullable=True)  # Правильный ответ (для тестов) в формате JSON
    order = Column(Integer, default=0)  # Порядок вопроса в тесте/анкете
    
    quiz = relationship("Quiz", back_populates="questions")
    user_answers = relationship("UserAnswer", back_populates="question", cascade="all, delete-orphan")

class UserQuizAttempt(Base):
    __tablename__ = "user_quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    score = Column(Integer, nullable=True)  # Результат в баллах (для тестов)
    
    user = relationship("User")
    quiz = relationship("Quiz")
    answers = relationship("UserAnswer", back_populates="attempt", cascade="all, delete-orphan")

class UserAnswer(Base):
    __tablename__ = "user_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("user_quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer = Column(JSON, nullable=False)  # Ответ пользователя в формате JSON
    is_correct = Column(Boolean, nullable=True)  # Правильность ответа (для тестов)
    
    attempt = relationship("UserQuizAttempt", back_populates="answers")
    question = relationship("Question", back_populates="user_answers")

