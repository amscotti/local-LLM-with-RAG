import requests
import json

# Базовый URL API
BASE_URL = "http://localhost:8000"

def test_create_quiz():
    """Тестирование создания нового теста"""
    # Данные для создания теста
    quiz_data = {
        "title": "Тестовый опрос по Python",
        "description": "Проверка знаний основ Python",
        "is_test": True,
        "department_id": None,
        "access_level": None,
        "questions": [
            {
                "text": "Какой тип данных используется для хранения последовательности элементов в Python?",
                "question_type": "single_choice",
                "options": [
                    {"id": 1, "text": "int"},
                    {"id": 2, "text": "str"},
                    {"id": 3, "text": "list"},
                    {"id": 4, "text": "dict"}
                ],
                "correct_answer": 3,
                "order": 1
            },
            {
                "text": "Выберите все встроенные типы данных в Python:",
                "question_type": "multiple_choice",
                "options": [
                    {"id": 1, "text": "int"},
                    {"id": 2, "text": "array"},
                    {"id": 3, "text": "dict"},
                    {"id": 4, "text": "varchar"}
                ],
                "correct_answer": [1, 3],
                "order": 2
            },
            {
                "text": "Как называется функция для получения длины объекта в Python?",
                "question_type": "text",
                "correct_answer": "len",
                "order": 3
            }
        ]
    }
    
    # Отправляем запрос на создание теста
    response = requests.post(f"{BASE_URL}/quiz/create", json=quiz_data)
    print("Создание теста:")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    return response.json()["id"] if response.status_code == 201 else None

def test_list_quizzes(user_id):
    """Тестирование получения списка тестов"""
    # Отправляем запрос на получение списка тестов
    response = requests.get(f"{BASE_URL}/quiz/list", params={"user_id": user_id})
    print("Список тестов:")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_get_quiz(quiz_id, user_id):
    """Тестирование получения информации о тесте"""
    # Отправляем запрос на получение информации о тесте
    response = requests.get(f"{BASE_URL}/quiz/{quiz_id}", params={"user_id": user_id})
    print(f"Информация о тесте {quiz_id}:")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_submit_attempt(quiz_id, user_id):
    """Тестирование отправки ответов на тест"""
    # Данные для отправки ответов
    attempt_data = {
        "quiz_id": quiz_id,
        "answers": [
            {
                "question_id": 1,  # ID первого вопроса (нужно заменить на реальный ID)
                "answer": 3  # Правильный ответ
            },
            {
                "question_id": 2,  # ID второго вопроса (нужно заменить на реальный ID)
                "answer": [1, 3]  # Правильный ответ
            },
            {
                "question_id": 3,  # ID третьего вопроса (нужно заменить на реальный ID)
                "answer": "len"  # Правильный ответ
            }
        ]
    }
    
    # Отправляем запрос на отправку ответов
    response = requests.post(f"{BASE_URL}/quiz/attempt", json=attempt_data, params={"user_id": user_id})
    print("Отправка ответов:")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    return response.json()["id"] if response.status_code == 201 else None

def test_get_user_attempts(user_id):
    """Тестирование получения списка попыток пользователя"""
    # Отправляем запрос на получение списка попыток
    response = requests.get(f"{BASE_URL}/quiz/attempts/{user_id}")
    print(f"Список попыток пользователя {user_id}:")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_get_attempt_details(attempt_id, user_id):
    """Тестирование получения детальной информации о попытке"""
    # Отправляем запрос на получение информации о попытке
    response = requests.get(f"{BASE_URL}/quiz/attempt/{attempt_id}", params={"user_id": user_id})
    print(f"Информация о попытке {attempt_id}:")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_get_quiz_statistics(quiz_id):
    """Тестирование получения статистики по тесту"""
    # Отправляем запрос на получение статистики
    response = requests.get(f"{BASE_URL}/quiz/stats/{quiz_id}")
    print(f"Статистика по тесту {quiz_id}:")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def run_tests():
    """Запуск всех тестов"""
    # ID пользователя для тестирования (нужно заменить на реальный ID)
    user_id = 1
    
    # Создаем тест
    quiz_id = test_create_quiz()
    if not quiz_id:
        print("Не удалось создать тест. Тестирование остановлено.")
        return
    
    # Получаем список тестов
    test_list_quizzes(user_id)
    
    # Получаем информацию о тесте
    test_get_quiz(quiz_id, user_id)
    
    # Отправляем ответы на тест
    attempt_id = test_submit_attempt(quiz_id, user_id)
    if not attempt_id:
        print("Не удалось отправить ответы. Тестирование остановлено.")
        return
    
    # Получаем список попыток пользователя
    test_get_user_attempts(user_id)
    
    # Получаем детальную информацию о попытке
    test_get_attempt_details(attempt_id, user_id)
    
    # Получаем статистику по тесту
    test_get_quiz_statistics(quiz_id)

if __name__ == "__main__":
    run_tests() 