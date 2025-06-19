from langchain_ollama import ChatOllama, OllamaEmbeddings
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Query, APIRouter
from pydantic import BaseModel
import uvicorn
import os
from sqlalchemy import create_engine, text, inspect, or_
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
import secrets
from typing import List
from fastapi.responses import FileResponse

from models_db import User, Department, Access, Content, Tag
from document_loader import load_documents_into_database, vec_search
import argparse
import sys
from database import get_db

from llm import getChatChain
from quiz import router as quiz_router
from directory_routes import router as directory_router  # Импортируйте ваш маршрутизатор
from llm_routes import router as llm_router  # Импортируйте ваш маршрутизатор
from content_routes import router as content_router
from user_routes import router as user_router

# Инициализация глобальных переменных
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)

# Добавляем маршрутизатор для тестов и анкет
app.include_router(quiz_router)
app.include_router(directory_router)
app.include_router(llm_router)  # Добавьте маршрутизатор для LL
app.include_router(content_router)
app.include_router(user_router)

# Словари для хранения экземпляров чатов и баз данных для каждого отдела
department_chats = {}  # {department_id: chat_instance}
department_dbs = {}    # {department_id: db_instance}
department_embedding_models = {}  # {department_id: embedding_model_instance}
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Настройки подключения к базе данных
DATABASE_URL = "mysql+mysqlconnector://root:123123@localhost:3306/db"

# Создание движка и сессии
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Добавляем новый класс для запросов на генерацию без RAG
class GenerateRequest(BaseModel):
    messages: str
    model: str = "ilyagusev/saiga_llama3:latest"

class GenerateResponse(BaseModel):
    text: str
    model: str = "ilyagusev/saiga_llama3:latest"

# Функция для проверки доступности модели
def check_if_model_is_available(model_name: str):
    # Список доступных моделей, можно расширить по необходимости
    available_models = [
        "ilyagusev/saiga_llama3:latest", 
        "snowflake-arctic-embed2:latest", 

    ]
    
    # Проверка доступности модели
    if model_name not in available_models:
        raise ValueError(f"Модель '{model_name}' недоступна. Доступные модели: {', '.join(available_models)}")
    
    return True

# Функция для получения списка доступных моделей
def get_available_models():
    # Список моделей LLM
    llm_models = [
        "ilyagusev/saiga_llama3:latest", 

    ]
    
    # Список моделей эмбеддингов
    embedding_models = [
        "snowflake-arctic-embed2:latest", 
    ]
    
    return {
        "llm_models": llm_models,
        "embedding_models": embedding_models
    }

# Эндпоинт для парсинга аргументов
@app.get("/parse-args")
async def parse_args():
    args = parse_arguments()
    return {
        "model": args.model,
        "embedding_model": args.embedding_model,
        "path": args.path,
        "web": args.web,
        "port": args.port
    }

@app.get("/check_db_connection")
async def check_db_connection():
    try:
        # Создаем сессию
        db = SessionLocal()
        # Выполняем простой запрос для проверки подключения
        db.execute(text("SELECT 1"))
        return {"message": "Подключение к базе данных успешно!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка подключения к базе данных: {str(e)}")
    finally:
        db.close()

def initialize_llm(llm_model_name: str, embedding_model_name: str, documents_path: str, department_id: str, reload: bool = False) -> bool:
    global department_chats, department_dbs, department_embedding_models
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
        print(f"База данных для отдела {department_id} успешно инициализирована.")
    except FileNotFoundError as e:
        print(f"Ошибка при загрузке документов: {e}")
        return False

    try:
        print("Создание LLM...")
        llm = ChatOllama(model=llm_model_name)
        department_chat = getChatChain(llm, department_dbs[department_id])
        department_chats[department_id] = department_chat
        print(f"LLM для отдела {department_id} успешно инициализирован.")
    except Exception as e:
        print(f"Ошибка при создании LLM: {e}")
        return False

    return True

def main(llm_model_name: str, embedding_model_name: str, documents_path: str, department_id: str = "default", web_mode: bool = False, port: int = 8000) -> None:
    print("Запуск функции main...")  # Отладочное сообщение
    print(f"Инициализация с параметрами:")  # Отладочное сообщение
    print(f"  Модель: {llm_model_name}")  # Отладочное сообщение
    print(f"  Модель встраивания: {embedding_model_name}")  # Отладочное сообщение
    print(f"  Путь к документам: {documents_path}")  # Отладочное сообщение
    print(f"  Отдел: {department_id}")  # Отладочное сообщение
    print(f"  Режим веб-сервера: {'включен' if web_mode else 'выключен'}")  # Отладочное сообщение
    print(f"  Порт: {port}")  # Отладочное сообщение

    success = initialize_llm(llm_model_name, embedding_model_name, documents_path, department_id)
    
    if not success:
        print("Не удалось инициализировать LLM. Завершение работы.")
        sys.exit(1)
    
    if web_mode:
        print(f"Запуск HTTP сервера на порту {port}...")
        print(f"Swagger UI доступен по адресу: http://0.0.0.0:{port}/docs")  # Отладочное сообщение
        uvicorn.run(app, host="0.0.0.0", port=port)
        print("Сервер успешно запущен.")  # Отладочное сообщение после запуска сервера
    else:
        # Консольный режим
        while True:
            try:
                user_input = input(
                    "\n\nPlease enter your question (or type 'exit' to end): "
                ).strip()
                if user_input.lower() == "exit":
                    break
                else:
                    department_chats[department_id](user_input)
            
            except KeyboardInterrupt:
                break

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local LLM with RAG with Ollama.")
    parser.add_argument(
        "-m",
        "--model",
        default="mistral",
        help="The name of the LLM model to use.",
    )
    parser.add_argument(
        "-e",
        "--embedding_model",
        default="nomic-embed-text",
        help="The name of the embedding model to use.",
    )
    parser.add_argument(
        "-p",
        "--path",
        default="Research",
        help="The path to the directory containing documents to load.",
    )
    parser.add_argument(
        "-d",
        "--department",
        default="default",
        help="The department ID to initialize the chat for.",
    )
    parser.add_argument(
        "-w",
        "--web",
        action="store_true",
        help="Run in web server mode instead of console mode.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for the web server (when using --web).",
    )
    return parser.parse_args()



@app.get("/api/departments")
async def get_departments(db: Session = Depends(get_db)):
    departments = db.query(Department).all()
    return [{"id": dept.id, "department_name": dept.department_name} for dept in departments]

@app.get("/api/access_levels")
async def get_access_levels(db: Session = Depends(get_db)):
    access_levels = db.query(Access).all()
    return [{"id": access_level.id, "access_name": access_level.access_name} for access_level in access_levels]

@app.get("/departments")
async def get_departments(db: Session = Depends(get_db)):
    departments = db.query(Department).all()
    return [{"id": dept.id, "name": dept.department_name} for dept in departments]

@app.get("/access-levels")
async def get_access_level(db: Session = Depends(get_db)):
    access_levels = db.query(Access).all()
    return [{"id": access.id, "access_name": access.access_name} for access in access_levels]

@app.get("/tables")
async def get_tables(db: Session = Depends(get_db)):
    try:
        inspector = inspect(db.bind)
        tables = inspector.get_table_names()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении таблиц: {str(e)}")

@app.get("/tables/{table_name}")
async def get_table_info(table_name: str, db: Session = Depends(get_db)):
    try:
        inspector = inspect(db.bind)
        columns = inspector.get_columns(table_name)
        return {"table": table_name, "columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении информации о таблице {table_name}: {str(e)}")

class TagCreate(BaseModel):
    tag_name: str

@app.post("/tags")
async def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    try:
        new_tag = Tag(tag_name=tag.tag_name)
        db.add(new_tag)
        db.commit()
        db.refresh(new_tag)
        return {"message": "Тег успешно добавлен", "tag": new_tag}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении тега: {str(e)}")

@app.get("/tags")
async def get_tags(db: Session = Depends(get_db)):
    try:
        tags = db.query(Tag).all()  # Получаем все теги из базы данных
        return {"tags": tags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении тегов: {str(e)}")

@app.get("/user/{user_id}/content/by-tags")
async def get_user_content_by_tags(user_id: int, db: Session = Depends(get_db)):
    try:
        # Получаем пользователя по user_id
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Получаем все теги
        tags = db.query(Tag).all()
        
        # Создаем словарь для результата
        result = {
            "tags": [],
            "untagged_content": []
        }
        
        # Добавляем информацию о тегах и связанном контенте
        for tag in tags:
            # Получаем контент для данного тега с учетом прав доступа пользователя
            tag_content = db.query(Content).filter(
                Content.tag_id == tag.id,
                Content.access_level == user.access_id,
                Content.department_id == user.department_id
            ).all()
            
            # Если есть контент для этого тега, добавляем его в результат
            if tag_content:
                tag_info = {
                    "id": tag.id,
                    "tag_name": tag.tag_name,
                    "content": []
                }
                
                for content in tag_content:
                    tag_info["content"].append({
                        "id": content.id,
                        "title": content.title,
                        "description": content.description,
                        "file_path": content.file_path
                    })
                
                result["tags"].append(tag_info)
        
        # Получаем контент без тега
        untagged_content = db.query(Content).filter(
            Content.tag_id == None,
            Content.access_level == user.access_id,
            Content.department_id == user.department_id
        ).all()
        
        # Добавляем контент без тега в результат
        for content in untagged_content:
            result["untagged_content"].append({
                "id": content.id,
                "title": content.title,
                "description": content.description,
                "file_path": content.file_path
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении контента: {str(e)}")


@app.get("/initialized-departments")
async def get_initialized_departments():
    """
    Возвращает список отделов, для которых уже инициализированы модели LLM.
    """
    departments = list(department_chats.keys())
    return {"departments": departments}

@app.get("/search-documents")
async def search_documents(
    user_id: int,
    search_query: str = Query(None, description="Поисковый запрос для названия, описания или имени файла"),
    db: Session = Depends(get_db)
):
    try:
        # Получаем пользователя по user_id для проверки прав доступа
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Базовый запрос с учетом прав доступа пользователя
        query = db.query(Content).filter(
            Content.access_level == user.access_id,
            Content.department_id == user.department_id
        )
        
        # Если указан поисковый запрос, добавляем условия поиска
        if search_query:
            # Получаем имя файла из пути
            query = query.filter(
                or_(
                    Content.title.ilike(f"%{search_query}%"),  # Поиск по названию
                    Content.description.ilike(f"%{search_query}%"),  # Поиск по описанию
                    Content.file_path.ilike(f"%{search_query}%")  # Поиск по пути файла (включая имя файла)
                )
            )
        
        # Выполняем запрос
        contents = query.all()
        
        # Если контент не найден, возвращаем пустой список
        if not contents:
            return {"documents": []}
        
        # Формируем результат
        result = []
        for content in contents:
            # Получаем имя файла из пути
            file_name = os.path.basename(content.file_path) if content.file_path else "Имя файла недоступно"
            
            # Получаем название отдела
            department = db.query(Department).filter(Department.id == content.department_id).first()
            department_name = department.department_name if department else "Неизвестный отдел"
            
            # Получаем название уровня доступа
            access = db.query(Access).filter(Access.id == content.access_level).first()
            access_name = access.access_name if access else "Неизвестный уровень"
            
            # Получаем название тега, если он есть
            tag_name = None
            if content.tag_id:
                tag = db.query(Tag).filter(Tag.id == content.tag_id).first()
                tag_name = tag.tag_name if tag else None
            
            result.append({
                "id": content.id,
                "title": content.title,
                "description": content.description,
                "file_path": content.file_path,
                "file_name": file_name,
                "department_id": content.department_id,
                "department_name": department_name,
                "access_level": content.access_level,
                "access_name": access_name,
                "tag_id": content.tag_id,
                "tag_name": tag_name
            })
        
        return {"documents": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при поиске документов: {str(e)}")

if __name__ == "__main__":
    args = parse_arguments()
    main(args.model, args.embedding_model, args.path, args.web, args.port)
