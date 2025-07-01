from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import datetime
import json

from database import get_db
from models_db import Quiz, Question, UserQuizAttempt, UserAnswer, User, Department, Access

router = APIRouter(prefix="/quiz", tags=["quiz"])

# Pydantic модели для запросов и ответов

class OptionBase(BaseModel):
    id: int
    text: str

class QuestionCreate(BaseModel):
    text: str
    question_type: str  # single_choice, multiple_choice, text
    options: Optional[List[Dict[str, Any]]] = None
    correct_answer: Optional[Any] = None
    order: Optional[int] = 0

class QuestionResponse(BaseModel):
    id: int
    text: str
    question_type: str
    options: Optional[List[Dict[str, Any]]] = None
    order: int
    
    class Config:
        orm_mode = True

class QuizCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_test: bool = False
    department_id: Optional[int] = None
    access_level: Optional[int] = None
    questions: List[QuestionCreate]

class QuizResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_test: bool
    department_id: Optional[int] = None
    access_level: Optional[int] = None
    created_at: datetime.datetime
    questions: List[QuestionResponse]
    
    class Config:
        orm_mode = True

class QuizListItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_test: bool
    department_id: Optional[int] = None
    access_level: Optional[int] = None
    created_at: datetime.datetime
    question_count: int
    
    class Config:
        orm_mode = True

class UserAnswerCreate(BaseModel):
    question_id: int
    answer: Any  # Может быть строкой, числом или списком (в зависимости от типа вопроса)

class AttemptCreate(BaseModel):
    quiz_id: int
    answers: List[UserAnswerCreate]

class UserAnswerResponse(BaseModel):
    id: int
    question_id: int
    answer: Any
    is_correct: Optional[bool] = None
    
    class Config:
        orm_mode = True

class AttemptResponse(BaseModel):
    id: int
    user_id: int
    quiz_id: int
    started_at: datetime.datetime
    completed_at: Optional[datetime.datetime] = None
    score: Optional[int] = None
    answers: List[UserAnswerResponse]
    
    class Config:
        orm_mode = True

class AttemptListItem(BaseModel):
    id: int
    quiz_id: int
    quiz_title: str
    started_at: datetime.datetime
    completed_at: Optional[datetime.datetime] = None
    score: Optional[int] = None
    total_questions: int
    correct_answers: Optional[int] = None
    
    class Config:
        orm_mode = True

# Функции для работы с тестами и анкетами

def check_user_access(user_id: int, quiz: Quiz, db: Session) -> bool:
    """Проверяет, имеет ли пользователь доступ к тесту/анкете"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    
    # Если тест/анкета не имеет ограничений по отделу и уровню доступа
    if quiz.department_id is None and quiz.access_level is None:
        return True
    
    # Проверка по отделу
    if quiz.department_id is not None and user.department_id != quiz.department_id:
        return False
    
    # Проверка по уровню доступа
    if quiz.access_level is not None and user.access_id < quiz.access_level:
        return False
    
    return True

def calculate_score(attempt_id: int, db: Session) -> int:
    """Рассчитывает количество баллов за тест"""
    attempt = db.query(UserQuizAttempt).filter(UserQuizAttempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Попытка не найдена")
    
    quiz = db.query(Quiz).filter(Quiz.id == attempt.quiz_id).first()
    if not quiz.is_test:
        return None  # Для анкет нет баллов
    
    correct_answers = db.query(UserAnswer).filter(
        UserAnswer.attempt_id == attempt_id,
        UserAnswer.is_correct == True
    ).count()
    
    return correct_answers

# Эндпоинты для работы с тестами и анкетами

@router.post("/create", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def create_quiz(quiz_data: QuizCreate, db: Session = Depends(get_db)):
    """Создание нового теста или анкеты"""
    # Проверка существования отдела и уровня доступа, если указаны
    if quiz_data.department_id:
        department = db.query(Department).filter(Department.id == quiz_data.department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail="Указанный отдел не найден")
    
    if quiz_data.access_level:
        access = db.query(Access).filter(Access.id == quiz_data.access_level).first()
        if not access:
            raise HTTPException(status_code=404, detail="Указанный уровень доступа не найден")
    
    # Создаем новый тест/анкету
    new_quiz = Quiz(
        title=quiz_data.title,
        description=quiz_data.description,
        is_test=quiz_data.is_test,
        department_id=quiz_data.department_id,
        access_level=quiz_data.access_level
    )
    
    db.add(new_quiz)
    db.flush()  # Чтобы получить ID нового теста/анкеты
    
    # Добавляем вопросы
    for i, question_data in enumerate(quiz_data.questions):
        # Преобразуем options и correct_answer в JSON, если они есть
        options_json = None
        if question_data.options:
            options_json = question_data.options
        
        correct_answer_json = None
        if question_data.correct_answer is not None:
            correct_answer_json = question_data.correct_answer
        
        new_question = Question(
            quiz_id=new_quiz.id,
            text=question_data.text,
            question_type=question_data.question_type,
            options=options_json,
            correct_answer=correct_answer_json,
            order=question_data.order or i
        )
        db.add(new_question)
    
    db.commit()
    
    # Получаем созданный тест/анкету со всеми вопросами
    created_quiz = db.query(Quiz).filter(Quiz.id == new_quiz.id).first()
    questions = db.query(Question).filter(Question.quiz_id == new_quiz.id).order_by(Question.order).all()
    
    # Формируем ответ
    result = QuizResponse(
        id=created_quiz.id,
        title=created_quiz.title,
        description=created_quiz.description,
        is_test=created_quiz.is_test,
        department_id=created_quiz.department_id,
        access_level=created_quiz.access_level,
        created_at=created_quiz.created_at,
        questions=[
            QuestionResponse(
                id=q.id,
                text=q.text,
                question_type=q.question_type,
                options=q.options,
                order=q.order
            ) for q in questions
        ]
    )
    
    return result

@router.get("/list", response_model=List[QuizListItem])
def list_quizzes(
    user_id: int,
    is_test: Optional[bool] = None,
    department_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Получение списка тестов и анкет с учетом прав доступа пользователя"""
    # Получаем информацию о пользователе
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Базовый запрос
    query = db.query(
        Quiz,
        func.count(Question.id).label("question_count")
    ).outerjoin(Question, Quiz.id == Question.quiz_id).group_by(Quiz.id)
    
    # Фильтр по типу (тест или анкета)
    if is_test is not None:
        query = query.filter(Quiz.is_test == is_test)
    
    # Фильтр по отделу
    if department_id:
        query = query.filter(Quiz.department_id == department_id)
    else:
        # Показываем тесты/анкеты, которые либо не привязаны к отделу,
        # либо привязаны к отделу пользователя
        query = query.filter((Quiz.department_id == None) | (Quiz.department_id == user.department_id))
    
    # Фильтр по уровню доступа
    query = query.filter((Quiz.access_level == None) | (Quiz.access_level <= user.access_id))
    
    # Получаем результаты
    results = query.all()
    
    # Формируем ответ
    quizzes = []
    for quiz, question_count in results:
        quizzes.append(QuizListItem(
            id=quiz.id,
            title=quiz.title,
            description=quiz.description,
            is_test=quiz.is_test,
            department_id=quiz.department_id,
            access_level=quiz.access_level,
            created_at=quiz.created_at,
            question_count=question_count
        ))
    
    return quizzes

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: int, user_id: int, db: Session = Depends(get_db)):
    """Получение информации о тесте/анкете по ID"""
    # Получаем тест/анкету
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Тест/анкета не найдена")
    
    # Проверяем права доступа
    if not check_user_access(user_id, quiz, db):
        raise HTTPException(status_code=403, detail="У вас нет доступа к этому тесту/анкете")
    
    # Получаем вопросы
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).order_by(Question.order).all()
    
    # Формируем ответ
    result = QuizResponse(
        id=quiz.id,
        title=quiz.title,
        description=quiz.description,
        is_test=quiz.is_test,
        department_id=quiz.department_id,
        access_level=quiz.access_level,
        created_at=quiz.created_at,
        questions=[
            QuestionResponse(
                id=q.id,
                text=q.text,
                question_type=q.question_type,
                options=q.options,
                order=q.order
            ) for q in questions
        ]
    )
    
    return result

@router.post("/attempt", response_model=AttemptResponse, status_code=status.HTTP_201_CREATED)
def submit_attempt(attempt_data: AttemptCreate, user_id: int, db: Session = Depends(get_db)):
    """Отправка ответов на тест/анкету"""
    # Получаем тест/анкету
    quiz = db.query(Quiz).filter(Quiz.id == attempt_data.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Тест/анкета не найдена")
    
    # Проверяем права доступа
    if not check_user_access(user_id, quiz, db):
        raise HTTPException(status_code=403, detail="У вас нет доступа к этому тесту/анкете")
    
    # Создаем новую попытку
    new_attempt = UserQuizAttempt(
        user_id=user_id,
        quiz_id=quiz.id,
        started_at=datetime.datetime.utcnow(),
        completed_at=datetime.datetime.utcnow()
    )
    
    db.add(new_attempt)
    db.flush()  # Чтобы получить ID новой попытки
    
    # Добавляем ответы пользователя
    for answer_data in attempt_data.answers:
        # Получаем вопрос
        question = db.query(Question).filter(Question.id == answer_data.question_id).first()
        if not question or question.quiz_id != quiz.id:
            raise HTTPException(status_code=400, detail=f"Вопрос {answer_data.question_id} не принадлежит этому тесту/анкете")
        
        # Проверяем правильность ответа (только для тестов)
        is_correct = None
        if quiz.is_test and question.correct_answer is not None:
            # Логика проверки зависит от типа вопроса
            if question.question_type == "single_choice":
                is_correct = answer_data.answer == question.correct_answer
            elif question.question_type == "multiple_choice":
                # Для множественного выбора сравниваем множества выбранных вариантов
                user_choices = set(answer_data.answer)
                correct_choices = set(question.correct_answer)
                is_correct = user_choices == correct_choices
            elif question.question_type == "text":
                # Для текстовых ответов можно сделать проверку на точное совпадение
                # или более сложную логику (например, регулярные выражения)
                is_correct = answer_data.answer.lower() == question.correct_answer.lower()
        
        # Создаем запись об ответе
        new_answer = UserAnswer(
            attempt_id=new_attempt.id,
            question_id=question.id,
            answer=answer_data.answer,
            is_correct=is_correct
        )
        
        db.add(new_answer)
    
    # Рассчитываем количество баллов (только для тестов)
    if quiz.is_test:
        db.flush()  # Чтобы сохранить ответы перед подсчетом баллов
        new_attempt.score = calculate_score(new_attempt.id, db)
    
    db.commit()
    
    # Получаем созданную попытку со всеми ответами
    attempt = db.query(UserQuizAttempt).filter(UserQuizAttempt.id == new_attempt.id).first()
    answers = db.query(UserAnswer).filter(UserAnswer.attempt_id == new_attempt.id).all()
    
    # Формируем ответ
    result = AttemptResponse(
        id=attempt.id,
        user_id=attempt.user_id,
        quiz_id=attempt.quiz_id,
        started_at=attempt.started_at,
        completed_at=attempt.completed_at,
        score=attempt.score,
        answers=[
            UserAnswerResponse(
                id=a.id,
                question_id=a.question_id,
                answer=a.answer,
                is_correct=a.is_correct
            ) for a in answers
        ]
    )
    
    return result

@router.get("/attempts/{user_id}", response_model=List[AttemptListItem])
def get_user_attempts(user_id: int, quiz_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Получение списка попыток пользователя"""
    # Проверяем существование пользователя
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Базовый запрос
    query = db.query(
        UserQuizAttempt,
        Quiz.title.label("quiz_title"),
        func.count(Question.id).label("total_questions"),
        func.sum(UserAnswer.is_correct.cast(Integer)).label("correct_answers")
    ).join(
        Quiz, UserQuizAttempt.quiz_id == Quiz.id
    ).outerjoin(
        Question, Quiz.id == Question.quiz_id
    ).outerjoin(
        UserAnswer, (UserAnswer.attempt_id == UserQuizAttempt.id) & (UserAnswer.question_id == Question.id)
    ).filter(
        UserQuizAttempt.user_id == user_id
    ).group_by(
        UserQuizAttempt.id, Quiz.title
    )
    
    # Фильтр по тесту/анкете
    if quiz_id:
        query = query.filter(UserQuizAttempt.quiz_id == quiz_id)
    
    # Получаем результаты
    results = query.all()
    
    # Формируем ответ
    attempts = []
    for attempt, quiz_title, total_questions, correct_answers in results:
        attempts.append(AttemptListItem(
            id=attempt.id,
            quiz_id=attempt.quiz_id,
            quiz_title=quiz_title,
            started_at=attempt.started_at,
            completed_at=attempt.completed_at,
            score=attempt.score,
            total_questions=total_questions or 0,
            correct_answers=correct_answers
        ))
    
    return attempts

@router.get("/attempt/{attempt_id}", response_model=AttemptResponse)
def get_attempt_details(attempt_id: int, user_id: int, db: Session = Depends(get_db)):
    """Получение детальной информации о попытке"""
    # Получаем попытку
    attempt = db.query(UserQuizAttempt).filter(UserQuizAttempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Попытка не найдена")
    
    # Проверяем права доступа (только владелец попытки может ее просмотреть)
    if attempt.user_id != user_id:
        raise HTTPException(status_code=403, detail="У вас нет доступа к этой попытке")
    
    # Получаем ответы
    answers = db.query(UserAnswer).filter(UserAnswer.attempt_id == attempt_id).all()
    
    # Формируем ответ
    result = AttemptResponse(
        id=attempt.id,
        user_id=attempt.user_id,
        quiz_id=attempt.quiz_id,
        started_at=attempt.started_at,
        completed_at=attempt.completed_at,
        score=attempt.score,
        answers=[
            UserAnswerResponse(
                id=a.id,
                question_id=a.question_id,
                answer=a.answer,
                is_correct=a.is_correct
            ) for a in answers
        ]
    )
    
    return result

@router.get("/stats/{quiz_id}")
def get_quiz_statistics(quiz_id: int, db: Session = Depends(get_db)):
    """Получение статистики по тесту/анкете"""
    # Получаем тест/анкету
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Тест/анкета не найдена")
    
    # Получаем количество попыток
    attempts_count = db.query(UserQuizAttempt).filter(UserQuizAttempt.quiz_id == quiz_id).count()
    
    # Получаем количество уникальных пользователей
    unique_users_count = db.query(UserQuizAttempt.user_id).filter(
        UserQuizAttempt.quiz_id == quiz_id
    ).distinct().count()
    
    # Для тестов получаем среднее количество баллов
    avg_score = None
    if quiz.is_test:
        avg_score_result = db.query(func.avg(UserQuizAttempt.score)).filter(
            UserQuizAttempt.quiz_id == quiz_id,
            UserQuizAttempt.score != None
        ).scalar()
        avg_score = float(avg_score_result) if avg_score_result else 0
    
    # Статистика по вопросам (только для тестов)
    question_stats = []
    if quiz.is_test:
        questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
        for question in questions:
            # Количество правильных ответов на вопрос
            correct_answers_count = db.query(UserAnswer).filter(
                UserAnswer.question_id == question.id,
                UserAnswer.is_correct == True
            ).count()
            
            # Общее количество ответов на вопрос
            total_answers_count = db.query(UserAnswer).filter(
                UserAnswer.question_id == question.id
            ).count()
            
            # Процент правильных ответов
            correct_percentage = (correct_answers_count / total_answers_count * 100) if total_answers_count > 0 else 0
            
            question_stats.append({
                "question_id": question.id,
                "text": question.text,
                "correct_answers": correct_answers_count,
                "total_answers": total_answers_count,
                "correct_percentage": correct_percentage
            })
    
    return {
        "quiz_id": quiz_id,
        "title": quiz.title,
        "is_test": quiz.is_test,
        "attempts_count": attempts_count,
        "unique_users_count": unique_users_count,
        "avg_score": avg_score,
        "question_stats": question_stats if quiz.is_test else None
    }

@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(quiz_id: int, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Удаление теста/анкеты"""
    # Получаем тест/анкету
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Тест/анкета не найдена")
    
    # Удаляем тест/анкету (каскадное удаление вопросов и попыток настроено в моделях)
    db.delete(quiz)
    db.commit()
    
    return None

@router.get("/admin/list", response_model=List[QuizListItem])
def list_all_quizzes(
    is_test: Optional[bool] = None,
    department_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Получение списка всех тестов и анкет для администратора без учета прав доступа"""
    # Базовый запрос
    query = db.query(
        Quiz,
        func.count(Question.id).label("question_count")
    ).outerjoin(Question, Quiz.id == Question.quiz_id).group_by(Quiz.id)
    
    # Фильтр по типу (тест или анкета)
    if is_test is not None:
        query = query.filter(Quiz.is_test == is_test)
    
    # Фильтр по отделу
    if department_id is not None:
        query = query.filter(Quiz.department_id == department_id)
    
    # Получаем результаты
    results = query.all()
    
    # Формируем ответ
    quizzes = []
    for quiz, question_count in results:
        quizzes.append(QuizListItem(
            id=quiz.id,
            title=quiz.title,
            description=quiz.description,
            is_test=quiz.is_test,
            department_id=quiz.department_id,
            access_level=quiz.access_level,
            created_at=quiz.created_at,
            question_count=question_count
        ))
    
    return quizzes 