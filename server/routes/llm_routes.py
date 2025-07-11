from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from langchain_ollama import ChatOllama
import traceback
import time
import asyncio
import uuid
from collections import defaultdict
from datetime import datetime, timedelta

from database import get_db
from models_db import Department
from document_loader import vec_search
from llm_state_manager import get_llm_state_manager

# Получаем единственный экземпляр менеджера
llm_state_manager = get_llm_state_manager()

# Создаем маршрутизатор
router = APIRouter(prefix="/llm", tags=["llm"])

# Константы для таймаутов
LLM_REQUEST_TIMEOUT = 120  # 2 минуты для LLM запросов
EMBEDDING_REQUEST_TIMEOUT = 30  # 30 секунд для embedding запросов

# Защита от рекурсии GET запросов
_get_request_counts = defaultdict(list)  # task_id -> [timestamps]
MAX_GET_REQUESTS_PER_MINUTE = 30  # Максимум 30 GET запросов в минуту к одной задаче

# Модели данных
class QueryRequest(BaseModel):
    question: str
    department_id: str = "default"

class QueryResponse(BaseModel):
    task_id: str
    status: str  # 'pending', 'processing', 'completed', 'failed'
    message: str

class QueryResultResponse(BaseModel):
    task_id: str
    status: str
    answer: str = ""
    chunks: List[str] = []
    files: List[str] = []
    error: str = ""
    created_at: str = ""
    started_at: str = ""
    completed_at: str = ""

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

class QueueStatusResponse(BaseModel):
    department_id: str
    initialized: bool
    max_concurrent: int = 0
    available_slots: int = 0
    processing_count: int = 0
    pending_count: int = 0
    total_active_tasks: int = 0

# Функция для асинхронного выполнения векторного поиска
async def async_vec_search(embedding_model, query, db, n_top_cos: int = 10):
    """Асинхронная обертка для vec_search"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, vec_search, embedding_model, query, db, n_top_cos)

# Функция для обработки задачи в фоне
async def process_query_task(task_id: str):
    """Асинхронно обрабатывает задачу запроса"""
    task = llm_state_manager.get_task_by_id(task_id)
    if not task:
        print(f"Задача {task_id} не найдена")
        return

    department_id = task.department_id
    user_question = task.question
    
    print(f"Начинаем обработку задачи {task_id} для отдела {department_id}")
    
    # Обновляем статус на "обработка"
    llm_state_manager.update_task_status(task_id, "processing")
    
    # Добавляем задачу в список активных
    with llm_state_manager.global_lock:
        if department_id not in llm_state_manager.active_tasks:
            llm_state_manager.active_tasks[department_id] = []
        llm_state_manager.active_tasks[department_id].append(task)
    
    # Получаем семафор для отдела
    semaphore = llm_state_manager.get_department_semaphore(department_id)
    
    if not semaphore:
        error_msg = f"Семафор для отдела {department_id} не найден"
        print(error_msg)
        llm_state_manager.update_task_status(task_id, "failed", error=error_msg)
        return
    
    # Ждем доступный слот в семафоре
    async with semaphore:
        try:
            start_time = time.time()
            
            # Получаем модель встраивания и базу данных
            embedding_model = llm_state_manager.get_department_embedding_model(department_id)
            department_db = llm_state_manager.get_department_db(department_id)
            
            if not embedding_model or not department_db:
                raise ValueError(f"Модель встраивания или база данных для отдела {department_id} не найдены")
            
            print(f"Задача {task_id}: Выполняем векторный поиск...")
            # Выполняем векторный поиск фрагментов асинхронно с тайм-аутом
            top_chunks, top_files = await asyncio.wait_for(
                async_vec_search(
                    embedding_model, 
                    user_question, 
                    department_db, 
                    n_top_cos=6  # Уменьшено для ускорения
                ),
                timeout=EMBEDDING_REQUEST_TIMEOUT
            )
            
            print(f"Задача {task_id}: Векторный поиск выполнен за {time.time() - start_time:.2f} секунд")
            
            # ЗНАЧИТЕЛЬНО увеличиваем паузу после embedding для предотвращения падений Ollama
            await asyncio.sleep(0.5)  # Минимальная пауза для переключения моделей
            
            if not top_chunks:
                print(f"Задача {task_id}: Векторный поиск не вернул результатов")
                top_chunks = ["Не найдено релевантных фрагментов для вашего запроса."]
                top_files = []
            
            # Получаем асинхронный экземпляр чата
            async_chat_instance = llm_state_manager.get_department_async_chat(department_id)
            
            if not async_chat_instance:
                raise ValueError(f"Асинхронный экземпляр чата для отдела {department_id} не найден")
            
            print(f"Задача {task_id}: Отправляем запрос к LLM...")
            # Устанавливаем таймаут для запроса к LLM
            response_start_time = time.time()
            
            # ЗНАЧИТЕЛЬНО увеличиваем паузу перед LLM запросом для Ollama
            await asyncio.sleep(0.2)  # Минимальная пауза перед LLM генерацией
            
            # Выполняем асинхронный запрос к LLM с тайм-аутом
            chat_result = await asyncio.wait_for(
                async_chat_instance(user_question),
                timeout=LLM_REQUEST_TIMEOUT
            )
            
            print(f"Задача {task_id}: Ответ от LLM получен за {time.time() - response_start_time:.2f} секунд")
            
            if not chat_result.get("success", True):
                print(f"Задача {task_id}: LLM вернул неуспешный результат")
                result = {
                    "answer": chat_result.get("answer", "Не удалось получить ответ от модели"),
                    "chunks": top_chunks,
                    "files": top_files
                }
            else:
                # Объединяем результаты векторного поиска и LLM
                result = {
                    "answer": chat_result.get("answer", ""),
                    "chunks": chat_result.get("chunks", top_chunks),
                    "files": chat_result.get("files", top_files)
                }
            
            total_time = time.time() - start_time
            print(f"Задача {task_id}: Общее время обработки: {total_time:.2f} секунд")
            
            # Обновляем статус на "завершено"
            llm_state_manager.update_task_status(task_id, "completed", result=result)
            
        except asyncio.TimeoutError:
            error_message = f"Задача {task_id}: превышен тайм-аут ({LLM_REQUEST_TIMEOUT} сек)"
            print(error_message)
            llm_state_manager.update_task_status(task_id, "failed", error=error_message)
        except Exception as e:
            error_message = f"Ошибка при обработке задачи {task_id}: {str(e)}"
            print(error_message)
            print(traceback.format_exc())
            
            # Обновляем статус на "ошибка"
            llm_state_manager.update_task_status(task_id, "failed", error=error_message)
        
        finally:
            # Удаляем задачу из списка активных
            with llm_state_manager.global_lock:
                if department_id in llm_state_manager.active_tasks:
                    try:
                        llm_state_manager.active_tasks[department_id].remove(task)
                    except ValueError:
                        pass  # Задача уже была удалена


# Эндпоинты

@router.post("/debug/query-request")
async def debug_query_request(request: QueryRequest):
    """
    Диагностический эндпоинт для отладки проблем с запросами.
    """
    try:
        department_id = request.department_id
        print(f"DEBUG: Получен запрос с department_id='{department_id}', question='{request.question[:50]}...'")
        
        # Проверяем инициализацию отдела
        is_initialized = llm_state_manager.is_department_initialized(department_id)
        print(f"DEBUG: Отдел {department_id} инициализирован: {is_initialized}")
        
        # Получаем список всех инициализированных отделов
        initialized_departments = llm_state_manager.get_initialized_departments()
        print(f"DEBUG: Инициализированные отделы: {initialized_departments}")
        
        # Проверяем состояние менеджера
        with llm_state_manager.global_lock:
            sync_chats = list(llm_state_manager.department_chats.keys())
            async_chats = list(llm_state_manager.department_async_chats.keys())
            databases = list(llm_state_manager.department_databases.keys())
            
        return {
            "request": {
                "department_id": department_id,
                "question": request.question[:100] + "..." if len(request.question) > 100 else request.question
            },
            "state": {
                "is_initialized": is_initialized,
                "initialized_departments": initialized_departments,
                "sync_chats": sync_chats,
                "async_chats": async_chats,
                "databases": databases
            }
        }
        
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

@router.get("/debug/department-state/{department_id}")
async def debug_department_state(department_id: str):
    """
    Диагностический эндпоинт для проверки состояния конкретного отдела.
    """
    try:
        is_initialized = llm_state_manager.is_department_initialized(department_id)
        is_partially = llm_state_manager.is_department_partially_initialized(department_id)
        
        with llm_state_manager.global_lock:
            state = {
                "department_id": department_id,
                "is_fully_initialized": is_initialized,
                "is_partially_initialized": is_partially,
                "components": {
                    "sync_chat": department_id in llm_state_manager.department_chats,
                    "async_chat": department_id in llm_state_manager.department_async_chats,
                    "database": department_id in llm_state_manager.department_databases,
                    "embedding": department_id in llm_state_manager.department_embedding_models,
                    "semaphore": department_id in llm_state_manager.department_semaphores,
                    "queue": department_id in llm_state_manager.department_queues,
                    "active_tasks": department_id in llm_state_manager.active_tasks
                }
            }
            
            # Добавляем информацию о количестве активных задач
            if department_id in llm_state_manager.active_tasks:
                active_tasks = llm_state_manager.active_tasks[department_id]
                state["active_tasks_count"] = len(active_tasks)
                state["task_statuses"] = [task.status for task in active_tasks]
            else:
                state["active_tasks_count"] = 0
                state["task_statuses"] = []
        
        return state
        
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

@router.post("/debug/reinitialize/{department_id}")
async def debug_reinitialize_department(department_id: str):
    """
    Принудительная переинициализация отдела при потере состояния.
    """
    try:
        print(f"DEBUG: Принудительная переинициализация отдела {department_id}")
        
        # Используем стандартные параметры для отдела 5
        if department_id == "5":
            success = llm_state_manager.initialize_llm(
                "gemma3",
                "nomic-embed-text", 
                "Research",
                department_id,
                reload=True
            )
        else:
            return {"error": f"Неизвестный отдел {department_id}. Поддерживается только отдел 5."}
        
        if success:
            return {
                "message": f"Отдел {department_id} успешно переинициализирован",
                "success": True
            }
        else:
            return {
                "message": f"Ошибка при переинициализации отдела {department_id}",
                "success": False
            }
            
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    Генерирует ответ на запрос без использования RAG.
    """
    try:
        # Проверяем, доступна ли модель
        llm_state_manager.check_if_model_is_available(request.model)
        
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

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest, background_tasks: BackgroundTasks):
    """
    Создает задачу для обработки запроса к LLM с использованием RAG.
    Возвращает task_id для отслеживания прогресса.
    """
    department_id = request.department_id
    print(f"API: Получен запрос для отдела '{department_id}', вопрос: '{request.question[:50]}...'")
    
    # Проверяем инициализацию отдела с детальным логированием
    is_initialized = llm_state_manager.is_department_initialized(department_id)
    print(f"API: Отдел '{department_id}' инициализирован: {is_initialized}")
    
    if not is_initialized:
        # Получаем дополнительную информацию для диагностики
        initialized_departments = llm_state_manager.get_initialized_departments()
        is_partially = llm_state_manager.is_department_partially_initialized(department_id)
        
        print(f"API: Доступные инициализированные отделы: {initialized_departments}")
        print(f"API: Отдел '{department_id}' частично инициализирован: {is_partially}")
        
        # Проверяем, все ли словари пусты (полная потеря состояния)
        with llm_state_manager.global_lock:
            sync_chats = list(llm_state_manager.department_chats.keys())
            async_chats = list(llm_state_manager.department_async_chats.keys())
            databases = list(llm_state_manager.department_databases.keys())
            embeddings = list(llm_state_manager.department_embedding_models.keys())
            
            print(f"API: Синхронные чаты: {sync_chats}")
            print(f"API: Асинхронные чаты: {async_chats}")
            
            total_components = len(sync_chats) + len(async_chats) + len(databases) + len(embeddings)
            
        # Если все словари пусты И это отдел 5, пытаемся автоматически восстановить
        if total_components == 0 and department_id == "5":
            print(f"WARNING: Обнаружена полная потеря состояния! Пытаемся автоматически восстановить отдел {department_id}")
            try:
                auto_restore_success = llm_state_manager.initialize_llm(
                    "gemma3",
                    "nomic-embed-text", 
                    "Research",
                    department_id,
                    reload=True
                )
                if auto_restore_success:
                    print(f"SUCCESS: Отдел {department_id} автоматически восстановлен!")
                    # Создаем задачу после успешного восстановления
                    task = llm_state_manager.create_query_task(department_id, request.question)
                    background_tasks.add_task(process_query_task, task.id)
                    return QueryResponse(
                        task_id=task.id,
                        status="pending",
                        message=f"Отдел {department_id} был автоматически восстановлен. Задача создана и добавлена в очередь обработки."
                    )
                else:
                    print(f"ERROR: Не удалось автоматически восстановить отдел {department_id}")
            except Exception as auto_restore_error:
                print(f"ERROR: Ошибка автоматического восстановления: {auto_restore_error}")
        
        # Разные сообщения в зависимости от состояния
        if is_partially:
            error_detail = (
                f"LLM для отдела '{department_id}' частично инициализирован (возможна race condition). "
                f"Попробуйте повторить запрос через несколько секунд или переинициализировать отдел через /llm/debug/reinitialize/{department_id}."
            )
        elif total_components == 0:
            error_detail = (
                f"Обнаружена полная потеря состояния LLM! Все отделы утратили инициализацию. "
                f"Автоматическое восстановление {'выполнено' if department_id == '5' else 'недоступно'}. "
                f"Для ручного восстановления используйте POST /llm/debug/reinitialize/{department_id}."
            )
        else:
            error_detail = (
                f"LLM для отдела '{department_id}' не инициализирован. "
                f"Доступные отделы: {initialized_departments}. "
                f"Инициализируйте отдел через POST /llm/initialize с параметрами: "
                f"model_name, embedding_model_name, documents_path, department_id='{department_id}'."
            )
        
        raise HTTPException(status_code=400, detail=error_detail)
    
    # Создаем новую задачу
    task = llm_state_manager.create_query_task(department_id, request.question)
    
    print(f"Создана задача {task.id} для отдела {department_id}: {request.question[:50]}...")
    
    # Запускаем обработку задачи в фоне
    background_tasks.add_task(process_query_task, task.id)
    
    return QueryResponse(
        task_id=task.id,
        status="pending",
        message=f"Задача создана и добавлена в очередь обработки для отдела {department_id}"
    )

def _check_get_request_rate_limit(task_id: str) -> bool:
    """Проверяет, не превышен ли лимит GET запросов для задачи"""
    now = datetime.now()
    one_minute_ago = now - timedelta(minutes=1)
    
    # Удаляем старые запросы (старше минуты)
    _get_request_counts[task_id] = [
        timestamp for timestamp in _get_request_counts[task_id] 
        if timestamp > one_minute_ago
    ]
    
    # Проверяем лимит
    if len(_get_request_counts[task_id]) >= MAX_GET_REQUESTS_PER_MINUTE:
        return False
    
    # Добавляем текущий запрос
    _get_request_counts[task_id].append(now)
    return True

@router.get("/query/{task_id}", response_model=QueryResultResponse)
async def get_query_result(task_id: str):
    """
    Получает результат выполнения задачи по её ID.
    Защищен от рекурсии чрезмерным количеством запросов.
    """
    # Защита от рекурсии GET запросов
    if not _check_get_request_rate_limit(task_id):
        raise HTTPException(
            status_code=429, 
            detail=f"Слишком много запросов к задаче {task_id}. Максимум {MAX_GET_REQUESTS_PER_MINUTE} запросов в минуту. Возможна рекурсия фронтенда."
        )
    
    task = llm_state_manager.get_task_by_id(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail=f"Задача с ID {task_id} не найдена")
    
    response = QueryResultResponse(
        task_id=task.id,
        status=task.status,
        created_at=task.created_at.isoformat() if task.created_at else "",
        started_at=task.started_at.isoformat() if task.started_at else "",
        completed_at=task.completed_at.isoformat() if task.completed_at else ""
    )
    
    if task.result:
        response.answer = task.result.get("answer", "")
        response.chunks = task.result.get("chunks", [])
        response.files = task.result.get("files", [])
    
    if task.error:
        response.error = task.error
    
    return response

@router.get("/queue/status/{department_id}", response_model=QueueStatusResponse)
async def get_queue_status(department_id: str):
    """
    Получает статус очереди для указанного отдела.
    """
    status = llm_state_manager.get_department_queue_status(department_id)
    return QueueStatusResponse(**status)

@router.post("/queue/cleanup/{department_id}")
async def cleanup_queue(department_id: str, max_age_minutes: int = 60):
    """
    Очищает завершенные задачи старше указанного времени для отдела.
    """
    llm_state_manager.cleanup_completed_tasks(department_id, max_age_minutes)
    return {"message": f"Очистка завершенных задач для отдела {department_id} выполнена"}

@router.post("/queue/force-cleanup/{department_id}")
async def force_cleanup_department(department_id: str):
    """
    Принудительно очищает все зависшие задачи и сбрасывает семафор для отдела.
    """
    try:
        result = llm_state_manager.force_cleanup_department(department_id)
        return {"message": f"Принудительная очистка отдела {department_id} выполнена", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при принудительной очистке: {str(e)}")

@router.post("/queue/force-cleanup-all")
async def force_cleanup_all_departments():
    """
    Принудительно очищает все зависшие задачи во всех отделах.
    """
    try:
        result = llm_state_manager.force_cleanup_all_departments()
        return {"message": "Принудительная очистка всех отделов выполнена", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при принудительной очистке: {str(e)}")

@router.get("/queue/stuck-tasks")
async def get_stuck_tasks(max_processing_minutes: int = 5):
    """
    Возвращает список зависших задач (обрабатываются дольше указанного времени).
    """
    try:
        stuck_tasks = llm_state_manager.get_stuck_tasks(max_processing_minutes)
        return {"stuck_tasks": stuck_tasks, "max_processing_minutes": max_processing_minutes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении зависших задач: {str(e)}")

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
        success = llm_state_manager.initialize_llm(
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
    models = llm_state_manager.get_available_models()
    return models

@router.get("/models/llm")
async def get_llm_models():
    """
    Возвращает список доступных моделей LLM.
    """
    models = llm_state_manager.get_available_models()
    return {"models": models["llm_models"]}

@router.get("/models/embedding")
async def get_embedding_models():
    """
    Возвращает список доступных моделей эмбеддингов.
    """
    models = llm_state_manager.get_available_models()
    return {"models": models["embedding_models"]}

@router.post("/query-sync")
async def query_sync(request: QueryRequest):
    """
    Синхронный запрос к LLM с использованием RAG для обратной совместимости.
    Этот эндпоинт блокирует выполнение до получения результата.
    """
    department_id = request.department_id
    
    # Проверяем инициализацию отдела
    if not llm_state_manager.is_department_initialized(department_id):
        raise HTTPException(
            status_code=400, 
            detail=f"LLM для отдела {department_id} не инициализирован. Сначала инициализируйте его через /llm/initialize."
        )
    
    # Создаем новую задачу
    task = llm_state_manager.create_query_task(department_id, request.question)
    
    print(f"Синхронная обработка задачи {task.id} для отдела {department_id}")
    
    # Сразу обрабатываем задачу
    await process_query_task(task.id)
    
    # Ждем завершения и возвращаем результат
    completed_task = llm_state_manager.get_task_by_id(task.id)
    
    if not completed_task:
        raise HTTPException(status_code=500, detail="Задача потеряна во время обработки")
    
    if completed_task.status == "failed":
        error_message = completed_task.error or "Неизвестная ошибка"
        return {
            "answer": f"Произошла ошибка при обработке запроса: {error_message}",
            "chunks": [],
            "files": []
        }
    
    if completed_task.status == "completed" and completed_task.result:
        return {
            "answer": completed_task.result.get("answer", ""),
            "chunks": completed_task.result.get("chunks", []),
            "files": completed_task.result.get("files", [])
        }
    
    # Если задача еще не завершена
    return {
        "answer": "Обработка не завершена, попробуйте позже",
        "chunks": [],
        "files": []
    }

@router.get("/initialized-departments")
async def get_initialized_departments():
    """
    Возвращает список отделов, для которых уже инициализированы модели LLM.
    """
    departments = llm_state_manager.get_initialized_departments()
    return {"departments": departments}
