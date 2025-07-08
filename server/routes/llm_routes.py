from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from langchain_ollama import ChatOllama, OllamaEmbeddings
import traceback
import time
from threading import Lock

from database import get_db
from models_db import Department
from document_loader import load_documents_into_database, vec_search

# Глобальные переменные для хранения экземпляров чатов и баз данных для каждого отдела
department_chats = {}  # {department_id: chat_instance}
department_dbs = {}    # {department_id: db_instance}
department_embedding_models = {}  # {department_id: embedding_model_instance}

# Блокировки для защиты от одновременных запросов к одному отделу
department_locks = {}  # {department_id: Lock()}

# Создаем маршрутизатор
router = APIRouter(prefix="/llm", tags=["llm"])

# Модели данных
class QueryRequest(BaseModel):
    question: str
    department_id: str = "default"

class InitRequest(BaseModel):
    model_name: str
    embedding_model_name: str
    documents_path: str
    department_id: str = "default"

class GenerateRequest(BaseModel):
    messages: str
    model: str = "gemma3"

class GenerateResponse(BaseModel):
    text: str
    model: str = "gemma3"

# Функция для проверки доступности модели
def check_if_model_is_available(model_name: str) -> bool:
    # Список доступных моделей, можно расширить по необходимости
    available_models = [
        "gemma3", 
        "nomic-embed-text",
        "ilyagusev/saiga_llama3:latest",
        "snowflake-arctic-embed2:latest",
    ]
    
    # Проверка доступности модели
    if model_name not in available_models:
        raise ValueError(f"Модель '{model_name}' недоступна. Доступные модели: {', '.join(available_models)}")
    
    return True

# Функция для получения списка доступных моделей
def get_available_models() -> Dict[str, List[str]]:
    # Список моделей LLM
    llm_models = [
        "gemma3",
        "ilyagusev/saiga_llama3:latest", 
    ]
    
    # Список моделей эмбеддингов
    embedding_models = [
        "nomic-embed-text",
        "snowflake-arctic-embed2:latest", 
    ]
    
    return {
        "llm_models": llm_models,
        "embedding_models": embedding_models
    }

# Функция для инициализации LLM
def initialize_llm(llm_model_name: str, embedding_model_name: str, documents_path: str, department_id: str, reload: bool = False) -> bool:
    global department_chats, department_dbs, department_embedding_models, department_locks
    print(f"Инициализация LLM для отдела {department_id}...")  # Отладочное сообщение
    try:
        print("Проверка доступности LLM модели...")
        check_if_model_is_available(llm_model_name)
        print("Проверка доступности модели встраивания...")
        check_if_model_is_available(embedding_model_name)
    except Exception as e:
        print(f"Ошибка при проверке доступности моделей: {e}")
        return False

    try:
        print(f"Загрузка документов в базу данных для отдела {department_id}...")
        department_db = load_documents_into_database(embedding_model_name, documents_path, department_id, reload=reload)
        # Сохраняем базу данных для этого отдела
        department_dbs[department_id] = department_db
        # Инициализируем модель встраивания для векторного поиска
        embedding_model = OllamaEmbeddings(model=embedding_model_name)
        department_embedding_models[department_id] = embedding_model
        # Создаем блокировку для отдела, если ее еще нет
        if department_id not in department_locks:
            department_locks[department_id] = Lock()
        print(f"База данных для отдела {department_id} успешно инициализирована.")
    except FileNotFoundError as e:
        print(f"Ошибка при загрузке документов: {e}")
        return False

    try:
        print("Создание LLM...")
        from llm import getChatChain
        llm = ChatOllama(model=llm_model_name)
        department_chat = getChatChain(llm, department_dbs[department_id])
        department_chats[department_id] = department_chat
        print(f"LLM для отдела {department_id} успешно инициализирован.")
    except Exception as e:
        print(f"Ошибка при создании LLM: {e}")
        return False

    return True

# Эндпоинты

@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    Генерирует ответ на запрос без использования RAG.
    """
    try:
        # Проверяем, доступна ли модель
        check_if_model_is_available(request.model)
        
        # Создаем экземпляр модели
        llm = ChatOllama(model=request.model)
        
        # Отправляем запрос напрямую к модели без использования RAG
        response = llm.invoke(request.messages)
        
        # Извлекаем ответ из объекта response
        if hasattr(response, "content"):
            response_text = response.content
        else:
            response_text = str(response)
            
        return GenerateResponse(text=response_text, model=request.model)
    except Exception as e:
        error_message = f"Ошибка при обработке запроса на генерацию: {str(e)}"
        print(error_message)
        print(traceback.format_exc())
        # Вместо ошибки 500 возвращаем ответ с сообщением об ошибке
        return GenerateResponse(
            text=f"Произошла ошибка при генерации ответа. Пожалуйста, попробуйте позже или переформулируйте вопрос. Детали: {str(e)}",
            model=request.model
        )

@router.post("/query")
async def query(request: QueryRequest):
    """
    Выполняет запрос к LLM с использованием RAG.
    """
    department_id = request.department_id
    
    if department_id not in department_chats:
        raise HTTPException(status_code=400, detail=f"LLM для отдела {department_id} не инициализирован. Сначала инициализируйте его через /llm/initialize.")
    
    # Получаем блокировку для отдела
    if department_id not in department_locks:
        department_locks[department_id] = Lock()
    
    # Проверяем, удалось ли получить блокировку
    if not department_locks[department_id].acquire(blocking=False):
        # Если блокировка уже занята, возвращаем ошибку занятости
        raise HTTPException(status_code=429, detail=f"LLM для отдела {department_id} сейчас занят обработкой другого запроса. Пожалуйста, повторите попытку позже.")
    
    try:
        print(f"Получен запрос для отдела {department_id}: {request}")  # Отладочное сообщение
        user_question = request.question
        
        start_time = time.time()
        
        try:
            # Выполняем векторный поиск фрагментов с таймаутом
            top_chunks, top_files = vec_search(
                department_embedding_models[department_id], 
                user_question, 
                department_dbs[department_id], 
                n_top_cos=5
            )
            
            print(f"Векторный поиск выполнен за {time.time() - start_time:.2f} секунд")
            
            if not top_chunks:
                print("Векторный поиск не вернул результатов")
                top_chunks = ["Не найдено релевантных фрагментов для вашего запроса."]
                top_files = []
                
        except Exception as e:
            error_message = f"Ошибка при векторном поиске: {str(e)}"
            print(error_message)
            print(traceback.format_exc())
            top_chunks = ["Произошла ошибка при поиске релевантных фрагментов."]
            top_files = []
        
        try:
            # Устанавливаем таймаут для запроса к LLM
            response_start_time = time.time()
            response = department_chats[department_id](user_question)
            print(f"Ответ от LLM получен за {time.time() - response_start_time:.2f} секунд")
            
            if response is None:
                print("Получен пустой ответ от LLM")
                return {"answer": "Не удалось получить ответ от модели. Пожалуйста, попробуйте позже или переформулируйте вопрос.", "chunks": top_chunks, "files": top_files}
            
            # Проверяем, начинается ли ответ с "Произошла ошибка"
            if isinstance(response, str) and response.startswith("Произошла ошибка"):
                print(f"LLM вернул сообщение об ошибке: {response}")
                # Возвращаем сообщение об ошибке как ответ, но с кодом 200
                return {"answer": "Произошла ошибка при генерации ответа. Пожалуйста, попробуйте позже или переформулируйте вопрос.", "chunks": top_chunks, "files": top_files}
            
            total_time = time.time() - start_time
            print(f"Общее время обработки запроса: {total_time:.2f} секунд")
            
            return {"answer": response, "chunks": top_chunks, "files": top_files}
        except Exception as e:
            error_message = f"Ошибка при обработке запроса: {str(e)}"
            print(error_message)
            print(traceback.format_exc())
            # Возвращаем сообщение об ошибке как ответ, но с кодом 200
            return {"answer": f"Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже или переформулируйте вопрос. Детали: {str(e)}", "chunks": top_chunks, "files": top_files}
    finally:
        # Освобождаем блокировку
        department_locks[department_id].release()

@router.post("/initialize")
async def initialize_model(request: InitRequest, db: Session = Depends(get_db)):
    """
    Инициализирует модель LLM для указанного отдела.
    """
    try:
        # Проверяем существование отдела в базе данных
        department = db.query(Department).filter(Department.id == int(request.department_id)).first()
        if not department and request.department_id != "default":
            raise HTTPException(status_code=404, detail=f"Отдел с ID {request.department_id} не найден")
        
        # Вызов функции инициализации с учетом отдела
        success = initialize_llm(
            request.model_name, 
            request.embedding_model_name, 
            request.documents_path, 
            request.department_id
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Не удалось инициализировать модель")
            
        return {"message": f"Модель для отдела {request.department_id} успешно инициализирована"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def get_models():
    """
    Возвращает список всех доступных моделей.
    """
    models = get_available_models()
    return models

@router.get("/models/llm")
async def get_llm_models():
    """
    Возвращает список доступных моделей LLM.
    """
    models = get_available_models()
    return {"models": models["llm_models"]}

@router.get("/models/embedding")
async def get_embedding_models():
    """
    Возвращает список доступных моделей эмбеддингов.
    """
    models = get_available_models()
    return {"models": models["embedding_models"]}

@router.get("/initialized-departments")
async def get_initialized_departments():
    """
    Возвращает список отделов, для которых уже инициализированы модели LLM.
    """
    departments = list(department_chats.keys())
    return {"departments": departments}
