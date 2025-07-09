"""
Централизованное управление состоянием LLM для всех отделов.
Этот модуль решает проблему дублирования глобальных переменных между app.py и llm_routes.py.
Добавлена поддержка параллельной обработки запросов и очередей.
"""

import os
import asyncio
import uuid
import threading
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from document_loader import load_documents_into_database
from llm import getChatChain, getAsyncChatChain

# Получение URL для Ollama из переменной окружения
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

@dataclass
class QueryTask:
    """Класс для представления задачи в очереди"""
    id: str
    department_id: str
    question: str
    status: str = "pending"  # pending, processing, completed, failed
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Глобальные переменные для синглтона
_llm_state_manager_instance = None
_llm_state_manager_lock = threading.Lock()

def get_llm_state_manager():
    """Thread-safe функция для получения единственного экземпляра LLMStateManager"""
    global _llm_state_manager_instance
    if _llm_state_manager_instance is None:
        with _llm_state_manager_lock:
            if _llm_state_manager_instance is None:
                print("DEBUG: Создаем ЕДИНСТВЕННЫЙ экземпляр LLMStateManager")
                _llm_state_manager_instance = LLMStateManager()
            else:
                print("DEBUG: Экземпляр уже создан во время ожидания блокировки")
    print(f"DEBUG: Возвращаем LLMStateManager с id: {id(_llm_state_manager_instance)}")
    return _llm_state_manager_instance

class LLMStateManager:
    """Управляет состоянием LLM отделов с поддержкой параллельной обработки"""
    
    def __init__(self):
        print(f"DEBUG: LLMStateManager.__init__ вызван, создаем экземпляр с id: {id(self)}")
        # Основные компоненты для каждого отдела
        self.department_llms = {}
        self.department_embedding_models = {}
        self.department_databases = {}
        self.department_chats = {}
        self.department_async_chats = {}
        
        # Управление очередями и семафорами  
        self.department_semaphores = {}
        self.department_queues = {}
        self.active_tasks = {}  # Словарь активных задач по отделам
        self.all_tasks = {}  # Все задачи (включая завершенные)
        
        # Настройки - ОПТИМИЗАЦИЯ скорости с сохранением стабильности  
        self.max_concurrent_requests_per_department = 3  # 3 запроса после оптимизации
        
        # Глобальная блокировка для thread-safety
        self.global_lock = threading.Lock()
        
        print("DEBUG: LLMStateManager успешно инициализирован")
    
    def check_if_model_is_available(self, model_name: str) -> bool:
        """Проверяет доступность модели"""
        available_models = [
            "gemma3",
            "nomic-embed-text",
            "ilyagusev/saiga_llama3:latest",
            "snowflake-arctic-embed2:latest",
        ]
        
        if model_name not in available_models:
            raise ValueError(f"Модель '{model_name}' недоступна. Доступные модели: {', '.join(available_models)}")
        
        return True
    
    def get_available_models(self) -> Dict[str, list]:
        """Возвращает список доступных моделей"""
        return {
            "llm_models": [
                "gemma3",
                "ilyagusev/saiga_llama3:latest",
            ],
            "embedding_models": [
                "nomic-embed-text",
                "snowflake-arctic-embed2:latest",
            ]
        }
    
    def initialize_llm(self, llm_model_name: str, embedding_model_name: str, 
                      documents_path: str, department_id: str, reload: bool = False) -> bool:
        """Инициализирует LLM для указанного отдела"""
        print(f"DEBUG: initialize_llm вызван для отдела {department_id}, id менеджера: {id(self)}")
        print(f"Инициализация LLM для отдела {department_id}...")
        
        # Проверяем, не был ли отдел уже инициализирован
        if not reload and self.is_department_initialized(department_id):
            print(f"WARNING: Отдел {department_id} уже инициализирован, пропускаем")
            return True
        
        try:
            # Проверяем доступность моделей
            print("Проверка доступности LLM модели...")
            self.check_if_model_is_available(llm_model_name)
            print("Проверка доступности модели встраивания...")
            self.check_if_model_is_available(embedding_model_name)
        except Exception as e:
            print(f"Ошибка при проверке доступности моделей: {e}")
            return False

        try:
            print(f"Загрузка документов в базу данных для отдела {department_id}...")
            department_db = load_documents_into_database(
                embedding_model_name, documents_path, department_id, reload=reload
            )
            
            # Используем глобальную блокировку для обновления словарей
            with self.global_lock:
                # Сохраняем базу данных для этого отдела
                self.department_databases[department_id] = department_db
                
                # Инициализируем модель встраивания для векторного поиска
                embedding_model = OllamaEmbeddings(
                    model=embedding_model_name, base_url=OLLAMA_HOST
                )
                self.department_embedding_models[department_id] = embedding_model
                
                # Создаем семафор для отдела, если его еще нет  
                if department_id not in self.department_semaphores:
                    self.department_semaphores[department_id] = asyncio.Semaphore(3)  # 3 параллельных запроса после оптимизации
                
                # Создаем очередь для отдела, если ее еще нет
                if department_id not in self.department_queues:
                    self.department_queues[department_id] = asyncio.Queue()
                
                # Инициализируем список активных задач для отдела
                if department_id not in self.active_tasks:
                    self.active_tasks[department_id] = []
            
            print(f"База данных для отдела {department_id} успешно инициализирована.")
        except FileNotFoundError as e:
            print(f"Ошибка при загрузке документов: {e}")
            return False

        try:
            print("Создание LLM...")
            llm = ChatOllama(
                model=llm_model_name, 
                base_url=OLLAMA_HOST,
                temperature=0.05,  # Минимальная креативность = максимальная скорость
                num_predict=256,  # Еще меньше токенов = быстрее генерация
                top_k=5,  # Минимум вариантов = максимум скорости
                top_p=0.8,  # Более строгая фокусировка
                repeat_penalty=1.1,  # Избегаем повторений
                num_thread=8,  # Используем больше потоков CPU
                num_batch=1  # Минимальный batch для скорости
            )
            department_chat = getChatChain(llm, self.department_databases[department_id])
            department_async_chat = getAsyncChatChain(llm, self.department_databases[department_id])
            
            # Используем глобальную блокировку для обновления словарей chats
            with self.global_lock:
                self.department_chats[department_id] = department_chat
                self.department_async_chats[department_id] = department_async_chat
            
            print(f"LLM для отдела {department_id} успешно инициализирован.")
        except Exception as e:
            print(f"Ошибка при создании LLM: {e}")
            return False

        return True
    
    def is_department_initialized(self, department_id: str) -> bool:
        """Проверяет, инициализирован ли отдел с исправлением неполной инициализации"""
        print(f"DEBUG: Проверяем инициализацию отдела {department_id}, id менеджера: {id(self)}")
        with self.global_lock:
            has_sync_chat = department_id in self.department_chats
            has_async_chat = department_id in self.department_async_chats
            has_database = department_id in self.department_databases
            has_embedding = department_id in self.department_embedding_models
            
            # Подсчитываем общее количество отделов в каждом словаре
            total_sync = len(self.department_chats)
            total_async = len(self.department_async_chats)  
            total_db = len(self.department_databases)
            total_emb = len(self.department_embedding_models)
            
            print(f"DEBUG: Состояние словарей: sync_chats={total_sync}, async_chats={total_async}, databases={total_db}, embeddings={total_emb}")
            
            # Полная инициализация требует наличия всех компонентов
            is_fully_initialized = all([has_sync_chat, has_async_chat, has_database, has_embedding])
            
            # Логируем состояние для диагностики
            if not is_fully_initialized:
                print(f"DEBUG: Неполная инициализация отдела {department_id}:")
                print(f"  - sync_chat: {has_sync_chat}")
                print(f"  - async_chat: {has_async_chat}")
                print(f"  - database: {has_database}")
                print(f"  - embedding: {has_embedding}")
                
                # Если есть хотя бы один компонент, но не все - это race condition
                has_any = any([has_sync_chat, has_async_chat, has_database, has_embedding])
                if has_any:
                    print(f"WARNING: Обнаружена частичная инициализация отдела {department_id}, может быть race condition")
                elif total_sync == 0 and total_async == 0 and total_db == 0 and total_emb == 0:
                    print(f"WARNING: ВСЕ СЛОВАРИ ПУСТЫ! Возможно, произошел сброс состояния менеджера!")
            
            return is_fully_initialized
    
    def is_department_partially_initialized(self, department_id: str) -> bool:
        """Проверяет, частично ли инициализирован отдел (для диагностики race conditions)"""
        with self.global_lock:
            components = [
                department_id in self.department_chats,
                department_id in self.department_async_chats,
                department_id in self.department_databases,
                department_id in self.department_embedding_models
            ]
            return any(components) and not all(components)
    
    def get_department_chat(self, department_id: str) -> Optional[Any]:
        """Получает экземпляр чата для отдела"""
        with self.global_lock:
            return self.department_chats.get(department_id)
    
    def get_department_async_chat(self, department_id: str) -> Optional[Any]:
        """Получает асинхронный экземпляр чата для отдела"""
        with self.global_lock:
            return self.department_async_chats.get(department_id)
    
    def get_department_db(self, department_id: str) -> Optional[Chroma]:
        """Получает базу данных для отдела"""
        with self.global_lock:
            return self.department_databases.get(department_id)
    
    def get_department_embedding_model(self, department_id: str) -> Optional[OllamaEmbeddings]:
        """Получает модель встраивания для отдела"""
        with self.global_lock:
            return self.department_embedding_models.get(department_id)
    
    def get_department_semaphore(self, department_id: str) -> asyncio.Semaphore:
        """Получает семафор для отдела, создавая его при необходимости"""
        with self.global_lock:
            if department_id not in self.department_semaphores:
                # 3 параллельных запроса после оптимизации
                self.department_semaphores[department_id] = asyncio.Semaphore(3)
            return self.department_semaphores[department_id]
    
    def get_department_queue(self, department_id: str) -> Optional[asyncio.Queue]:
        """Получает очередь для отдела"""
        with self.global_lock:
            if department_id not in self.department_queues:
                self.department_queues[department_id] = asyncio.Queue()
            return self.department_queues.get(department_id)
    
    def create_query_task(self, department_id: str, question: str) -> QueryTask:
        """Создает новую задачу запроса"""
        task_id = str(uuid.uuid4())
        task = QueryTask(
            id=task_id,
            department_id=department_id,
            question=question
        )
        
        with self.global_lock:
            self.all_tasks[task_id] = task
            if department_id not in self.active_tasks:
                self.active_tasks[department_id] = []
        
        return task
    
    def get_task_by_id(self, task_id: str) -> Optional[QueryTask]:
        """Получает задачу по ID"""
        with self.global_lock:
            return self.all_tasks.get(task_id)
    
    def update_task_status(self, task_id: str, status: str, result: Optional[Dict[str, Any]] = None, error: Optional[str] = None):
        """Обновляет статус задачи"""
        with self.global_lock:
            task = self.all_tasks.get(task_id)
            if task:
                task.status = status
                if status == "processing" and not task.started_at:
                    task.started_at = datetime.now()
                elif status in ["completed", "failed"]:
                    task.completed_at = datetime.now()
                
                if result:
                    task.result = result
                if error:
                    task.error = error
    
    def get_department_queue_status(self, department_id: str) -> Dict[str, Any]:
        """Получает статус очереди для отдела"""
        with self.global_lock:
            semaphore = self.department_semaphores.get(department_id)
            active_tasks = self.active_tasks.get(department_id, [])
            
            # Фильтруем активные задачи по статусу
            processing_tasks = [t for t in active_tasks if t.status == "processing"]
            pending_tasks = [t for t in active_tasks if t.status == "pending"]
            
            # Обновляем максимальное количество одновременных запросов
            max_concurrent = 3  # Оптимизированная параллельная обработка
            available_slots = max_concurrent - len(processing_tasks) if semaphore else 0
            
            return {
                "department_id": department_id,
                "initialized": self.is_department_initialized(department_id),
                "max_concurrent": max_concurrent,
                "available_slots": max(0, available_slots),
                "processing_count": len(processing_tasks),
                "pending_count": len(pending_tasks),
                "total_active_tasks": len(active_tasks)
            }
    
    def cleanup_completed_tasks(self, department_id: str, max_age_minutes: int = 60):
        """Очищает завершенные задачи старше указанного времени"""
        now = datetime.now()
        with self.global_lock:
            if department_id in self.active_tasks:
                tasks_to_remove = []
                for task in self.active_tasks[department_id]:
                    if task.status in ["completed", "failed"] and task.completed_at:
                        age = (now - task.completed_at).total_seconds() / 60
                        if age > max_age_minutes:
                            tasks_to_remove.append(task)
                
                # Удаляем старые задачи
                for task in tasks_to_remove:
                    self.active_tasks[department_id].remove(task)
                    if task.id in self.all_tasks:
                        del self.all_tasks[task.id]
                
                print(f"Очищено {len(tasks_to_remove)} завершенных задач для отдела {department_id}")
    
    def get_initialized_departments(self) -> list:
        """Возвращает список инициализированных отделов"""
        with self.global_lock:
            # Возвращаем отделы, которые инициализированы и для синхронных, и для асинхронных чатов
            sync_departments = set(self.department_chats.keys())
            async_departments = set(self.department_async_chats.keys())
            return list(sync_departments.intersection(async_departments))
    
    def remove_department(self, department_id: str) -> bool:
        """Удаляет отдел из состояния"""
        with self.global_lock:
            removed = False
            if department_id in self.department_chats:
                del self.department_chats[department_id]
                removed = True
            if department_id in self.department_async_chats:
                del self.department_async_chats[department_id]
            if department_id in self.department_databases:
                del self.department_databases[department_id]
            if department_id in self.department_embedding_models:
                del self.department_embedding_models[department_id]
            if department_id in self.department_semaphores:
                del self.department_semaphores[department_id]
            if department_id in self.department_queues:
                del self.department_queues[department_id]
            if department_id in self.active_tasks:
                # Удаляем все задачи отдела из общего словаря
                for task in self.active_tasks[department_id]:
                    if task.id in self.all_tasks:
                        del self.all_tasks[task.id]
                del self.active_tasks[department_id]
            return removed
    
    def force_cleanup_department(self, department_id: str) -> Dict[str, Any]:
        """Принудительно очищает все зависшие задачи отдела и сбрасывает семафор"""
        with self.global_lock:
            cleaned_tasks = 0
            failed_tasks = 0
            
            # Получаем список активных задач для отдела
            if department_id in self.active_tasks:
                tasks_to_cleanup = []
                for task in self.active_tasks[department_id]:
                    if task.status in ["pending", "processing"]:
                        tasks_to_cleanup.append(task)
                
                # Помечаем все незавершенные задачи как failed
                for task in tasks_to_cleanup:
                    if task.status == "processing":
                        task.status = "failed"
                        task.error = "Задача принудительно завершена из-за зависания"
                        task.completed_at = datetime.now()
                        failed_tasks += 1
                    else:
                        # Удаляем pending задачи полностью
                        self.active_tasks[department_id].remove(task)
                        if task.id in self.all_tasks:
                            del self.all_tasks[task.id]
                        cleaned_tasks += 1
            
            # Пересоздаем семафор для отдела
            if department_id in self.department_semaphores:
                del self.department_semaphores[department_id]
            self.department_semaphores[department_id] = asyncio.Semaphore(1)  # ТОЛЬКО 1!
            
            print(f"Принудительная очистка отдела {department_id}: "
                  f"очищено {cleaned_tasks} задач, отмечено как failed {failed_tasks} задач")
            
            return {
                "department_id": department_id,
                "cleaned_tasks": cleaned_tasks,
                "failed_tasks": failed_tasks,
                "semaphore_reset": True
            }
    
    def force_cleanup_all_departments(self) -> Dict[str, Any]:
        """Принудительно очищает все зависшие задачи во всех отделах"""
        total_cleaned = 0
        total_failed = 0
        departments_processed = []
        
        with self.global_lock:
            # Получаем список всех отделов
            all_departments = set()
            all_departments.update(self.active_tasks.keys())
            all_departments.update(self.department_semaphores.keys())
            
            for department_id in all_departments:
                # Временно освобождаем блокировку для вызова force_cleanup_department
                pass
        
        # Очищаем каждый отдел по отдельности
        for department_id in all_departments:
            result = self.force_cleanup_department(department_id)
            departments_processed.append(department_id)
            total_cleaned += result["cleaned_tasks"]
            total_failed += result["failed_tasks"]
        
        print(f"Принудительная очистка всех отделов: "
              f"обработано {len(departments_processed)} отделов, "
              f"очищено {total_cleaned} задач, отмечено как failed {total_failed} задач")
        
        return {
            "departments_processed": departments_processed,
            "total_cleaned_tasks": total_cleaned,
            "total_failed_tasks": total_failed,
            "total_departments": len(departments_processed)
        }
    
    def get_stuck_tasks(self, max_processing_minutes: int = 5) -> Dict[str, List[str]]:
        """Возвращает список зависших задач (processing > max_processing_minutes)"""
        now = datetime.now()
        stuck_tasks = {}
        
        with self.global_lock:
            for department_id, tasks in self.active_tasks.items():
                department_stuck = []
                for task in tasks:
                    if (task.status == "processing" and 
                        task.started_at and 
                        (now - task.started_at).total_seconds() / 60 > max_processing_minutes):
                        department_stuck.append(task.id)
                
                if department_stuck:
                    stuck_tasks[department_id] = department_stuck
        
        return stuck_tasks

# Получаем единственный экземпляр менеджера состояния через функцию
llm_state_manager = get_llm_state_manager() 