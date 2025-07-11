import os
import sys
import time
from utils.rabbitmq_service import RabbitMQService
from langchain_ollama import ChatOllama, OllamaEmbeddings

# Импортируем необходимые модули из вашего проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db
from document_loader import vec_search

# Глобальные переменные для хранения экземпляров чатов и баз данных
department_chats = {}
department_dbs = {}
department_embedding_models = {}

def process_llm_query(message):
    """Обрабатывает запрос к LLM из очереди RabbitMQ"""
    question = message.get("question")
    department_id = message.get("department_id", "default")
    user_id = message.get("user_id")
    
    # Здесь должна быть логика обработки запроса к LLM
    # Это может быть тот же код, который у вас уже есть в маршруте /llm/query
    # Но адаптированный для работы вне контекста HTTP запроса
    
    print(f"Обработка запроса: {question} от пользователя {user_id} для отдела {department_id}")
    
    # Пример обработки запроса (замените на вашу логику)
    # Здесь должен быть ваш код для работы с LLM

if __name__ == "__main__":
    rabbitmq_service = RabbitMQService()
    
    print("Запуск обработчика сообщений...")
    
    # Попытка подключения к RabbitMQ с повторами
    connected = False
    while not connected:
        try:
            rabbitmq_service.connect()
            connected = True
        except Exception as e:
            print(f"Не удалось подключиться к RabbitMQ: {e}")
            print("Повторная попытка через 5 секунд...")
            time.sleep(5)
    
    print("Подключено к RabbitMQ, ожидание сообщений...")
    
    try:
        # Начинаем прослушивать очередь
        rabbitmq_service.consume_messages("llm_queries", process_llm_query)
    except KeyboardInterrupt:
        print("Остановка обработчика сообщений...")
        rabbitmq_service.close()

