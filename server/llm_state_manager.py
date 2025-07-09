"""
Централизованное управление состоянием LLM для всех отделов.
Этот модуль решает проблему дублирования глобальных переменных между app.py и llm_routes.py.
"""

import os
from threading import Lock
from typing import Dict, Any, Optional
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from document_loader import load_documents_into_database
from llm import getChatChain

# Получение URL для Ollama из переменной окружения
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

class LLMStateManager:
    """Синглтон для управления состоянием LLM отделов"""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(LLMStateManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            # Словари для хранения экземпляров чатов и баз данных для каждого отдела
            self.department_chats: Dict[str, Any] = {}
            self.department_dbs: Dict[str, Chroma] = {}
            self.department_embedding_models: Dict[str, OllamaEmbeddings] = {}
            
            # Блокировки для защиты от одновременных запросов к одному отделу
            self.department_locks: Dict[str, Lock] = {}
            
            # Глобальная блокировка для защиты доступа к словарям
            self.global_lock = Lock()
            
            self._initialized = True
    
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
        print(f"Инициализация LLM для отдела {department_id}...")
        
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
                self.department_dbs[department_id] = department_db
                
                # Инициализируем модель встраивания для векторного поиска
                embedding_model = OllamaEmbeddings(
                    model=embedding_model_name, base_url=OLLAMA_HOST
                )
                self.department_embedding_models[department_id] = embedding_model
                
                # Создаем блокировку для отдела, если ее еще нет
                if department_id not in self.department_locks:
                    self.department_locks[department_id] = Lock()
            
            print(f"База данных для отдела {department_id} успешно инициализирована.")
        except FileNotFoundError as e:
            print(f"Ошибка при загрузке документов: {e}")
            return False

        try:
            print("Создание LLM...")
            llm = ChatOllama(model=llm_model_name, base_url=OLLAMA_HOST)
            department_chat = getChatChain(llm, self.department_dbs[department_id])
            
            # Используем глобальную блокировку для обновления словаря department_chats
            with self.global_lock:
                self.department_chats[department_id] = department_chat
            
            print(f"LLM для отдела {department_id} успешно инициализирован.")
        except Exception as e:
            print(f"Ошибка при создании LLM: {e}")
            return False

        return True
    
    def is_department_initialized(self, department_id: str) -> bool:
        """Проверяет, инициализирован ли отдел"""
        with self.global_lock:
            return department_id in self.department_chats
    
    def get_department_chat(self, department_id: str) -> Optional[Any]:
        """Получает экземпляр чата для отдела"""
        with self.global_lock:
            return self.department_chats.get(department_id)
    
    def get_department_db(self, department_id: str) -> Optional[Chroma]:
        """Получает базу данных для отдела"""
        with self.global_lock:
            return self.department_dbs.get(department_id)
    
    def get_department_embedding_model(self, department_id: str) -> Optional[OllamaEmbeddings]:
        """Получает модель встраивания для отдела"""
        with self.global_lock:
            return self.department_embedding_models.get(department_id)
    
    def get_department_lock(self, department_id: str) -> Optional[Lock]:
        """Получает блокировку для отдела"""
        with self.global_lock:
            if department_id not in self.department_locks:
                self.department_locks[department_id] = Lock()
            return self.department_locks.get(department_id)
    
    def get_initialized_departments(self) -> list:
        """Возвращает список инициализированных отделов"""
        with self.global_lock:
            return list(self.department_chats.keys())
    
    def remove_department(self, department_id: str) -> bool:
        """Удаляет отдел из состояния"""
        with self.global_lock:
            removed = False
            if department_id in self.department_chats:
                del self.department_chats[department_id]
                removed = True
            if department_id in self.department_dbs:
                del self.department_dbs[department_id]
            if department_id in self.department_embedding_models:
                del self.department_embedding_models[department_id]
            if department_id in self.department_locks:
                del self.department_locks[department_id]
            return removed

# Создаем глобальный экземпляр менеджера состояния
llm_state_manager = LLMStateManager() 