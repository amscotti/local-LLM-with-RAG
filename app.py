from langchain_ollama import ChatOllama, OllamaEmbeddings
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel
import uvicorn
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
import secrets
from typing import List
from fastapi.responses import FileResponse

from models_db import User, Department, Access, Content
from document_loader import load_documents_into_database, vec_search
import argparse
import sys
from database import get_db

from llm import getChatChain

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

# Инициализация глобальных переменных
app = FastAPI()
chat = None
db = None
embedding_model = None
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

# Добавляем новый эндпоинт для генерации без использования RAG
@app.post("/generate")
async def generate(request: GenerateRequest):
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
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_message)
    



# Эндпоинт для векторного поиска
class QueryRequest(BaseModel):
    question: str

class InitRequest(BaseModel):
    model_name: str
    embedding_model_name: str
    documents_path: str
    reload: bool = False

@app.post("/query")
async def query(request: QueryRequest):
    global chat
    if chat is None:
        raise HTTPException(status_code=500, detail="LLM не инициализирован. Запустите сервер с правильными параметрами.")
    
    print(f"Получен запрос: {request}")  # Отладочное сообщение
    user_question = request.question
    
    # Выполняем векторный поиск фрагментов
    top_chunks, top_files = vec_search(embedding_model, user_question, db, n_top_cos=5)
    
    try:
        response = chat(user_question)
        print(f"Ответ от LLM: {response}")  # Отладочное сообщение
        
        if response is None:
            print("Получен пустой ответ от LLM")
            raise HTTPException(status_code=500, detail="Получен пустой ответ от LLM.")
        
        # Проверяем, начинается ли ответ с "Произошла ошибка"
        if isinstance(response, str) and response.startswith("Произошла ошибка"):
            print(f"LLM вернул сообщение об ошибке: {response}")
            raise HTTPException(status_code=500, detail=response)
        
        return {"answer": response, "chunks": top_chunks, "files": top_files}
    except Exception as e:
        error_message = f"Ошибка при обработке запроса: {str(e)}"
        print(error_message)
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_message)


# Эндпоинт для инициализации LLM
@app.post("/initialize")
async def initialize(request: InitRequest):
    success = initialize_llm(request.model_name, request.embedding_model_name, request.documents_path, reload=request.reload)
    
    if not success:
        raise HTTPException(status_code=500, detail="Не удалось инициализировать LLM.")
    return {"message": "LLM успешно инициализирован."}

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

# Эндпоинт для получения всех доступных моделей
@app.get("/models")
async def get_models():
    models = get_available_models()
    return models

# Эндпоинт для получения доступных моделей LLM
@app.get("/models/llm")
async def get_llm_models():
    models = get_available_models()
    return {"models": models["llm_models"]}

# Эндпоинт для получения доступных моделей эмбеддингов
@app.get("/models/embedding")
async def get_embedding_models():
    models = get_available_models()
    return {"models": models["embedding_models"]}

# Эндпоинт для загрузки файлов
@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    # Проверка на уникальность имени файла
    if file.filename in os.listdir("Research"):  # Предполагается, что "Research" - это папка для хранения файлов
        return {"message": "Файл с таким именем уже существует."}

    # Сохранение файла
    file_location = f"Research/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    return {"message": f"Файл '{file.filename}' успешно загружен."}

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

def initialize_llm(llm_model_name: str, embedding_model_name: str, documents_path: str, reload: bool = False) -> bool:
    global chat, db, embedding_model
    print("Инициализация LLM...")  # Отладочное сообщение
    try:
        print("Проверка доступности LLM модели...")
        check_if_model_is_available(llm_model_name)
        print("Проверка доступности модели встраивания...")
        check_if_model_is_available(embedding_model_name)
    except Exception as e:
        print(f"Ошибка при проверке доступности моделей: {e}")
        return False

    try:
        print("Загрузка документов в базу данных...")
        db = load_documents_into_database(embedding_model_name, documents_path, reload=reload)
        # Инициализируем модель встраивания для векторного поиска
        embedding_model = OllamaEmbeddings(model=embedding_model_name)
        print("База данных успешно инициализирована.")
    except FileNotFoundError as e:
        print(f"Ошибка при загрузке документов: {e}")
        return False

    try:
        print("Создание LLM...")
        llm = ChatOllama(model=llm_model_name)
        chat = getChatChain(llm, db)
        print("LLM успешно инициализирован.")
    except Exception as e:
        print(f"Ошибка при создании LLM: {e}")
        return False

    return True

def main(llm_model_name: str, embedding_model_name: str, documents_path: str, web_mode: bool = False, port: int = 8000) -> None:
    print("Запуск функции main...")  # Отладочное сообщение
    print(f"Инициализация с параметрами:")  # Отладочное сообщение
    print(f"  Модель: {llm_model_name}")  # Отладочное сообщение
    print(f"  Модель встраивания: {embedding_model_name}")  # Отладочное сообщение
    print(f"  Путь к документам: {documents_path}")  # Отладочное сообщение
    print(f"  Режим веб-сервера: {'включен' if web_mode else 'выключен'}")  # Отладочное сообщение
    print(f"  Порт: {port}")  # Отладочное сообщение

    success = initialize_llm(llm_model_name, embedding_model_name, documents_path)
    
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
                    chat(user_input)
            
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

class UserCreate(BaseModel):
    login: str
    password: str
    role_id: int
    department_id: int
    access_id: int
# role_id - 1
# department_id - 5
# access_id - 3

@app.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Проверка существования пользователя
    existing_user = db.query(User).filter(User.login == user.login).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    # Хеширование пароля
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        login=user.login,
        password=hashed_password,
        role_id=user.role_id,
        department_id=user.department_id,
        access_id=user.access_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Пользователь успешно зарегистрирован"}

class UserLogin(BaseModel):
    login: str
    password: str

def generate_auth_key() -> str:
    """Генерация случайного ключа аутентификации."""
    return secrets.token_hex(16)

@app.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == user_data.login).first()
    if not user or not user.check_password(user_data.password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    auth_key = generate_auth_key()
    user.auth_key = auth_key
    db.commit()
    
    return {
        "id": user.id,
        "login": user.login,
        "auth_key": auth_key,
        "role_id": user.role_id,
        "department_id": user.department_id,
        "access_id": user.access_id
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)

@app.post("/upload-content")
async def upload_content(title: str, description: str, access_id: int, department_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Сохранение файла на сервере
    file_location = f"content_files/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Проверка существования уровня доступа
    access = db.query(Access).filter(Access.id == access_id).first()
    if access is None:
        raise HTTPException(status_code=400, detail="Уровень доступа не найден")

    # Создание записи в базе данных
    new_content = Content(
        title=title,
        description=description,
        file_path=file_location,
        access_level=access_id,
        department_id=department_id
    )
    db.add(new_content)
    db.commit()
    db.refresh(new_content)

    return {"message": "Контент успешно загружен"}





class ContentBase(BaseModel):
    id: int
    title: str
    description: str
    file_path: str

    class Config:
        orm_mode = True

@app.get("/content/filter", response_model=List[ContentBase])
async def get_content_by_access_and_department(access_level: int, department_id: int, db: Session = Depends(get_db)):
    try:
        # Получаем контент из базы данных по access_level и department_id
        contents = db.query(Content).filter(
            Content.access_level == access_level,
            Content.department_id == department_id
        ).all()

        if not contents:
            raise HTTPException(status_code=404, detail="Контент не найден")

        return [
            ContentBase(
                id=content.id,
                title=content.title,
                description=content.description,
                file_path=content.file_path
            ) for content in contents
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении контента: {str(e)}")
    
@app.get("/user/{id}")
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Получаем название отдела
    department = db.query(Department).filter(Department.id == user.department_id).first()
    department_name = department.department_name if department else "Неизвестный отдел"

    # Получаем название доступа
    access = db.query(Access).filter(Access.id == user.access_id).first()
    access_name = access.access_name if access else "Неизвестный доступ"

    return {
        "login": user.login,
        "role_id": user.role_id,
        "department_name": department_name,
        "access_name": access_name,
    }

@app.get("/user/{user_id}/content")
async def get_user_content(user_id: int, db: Session = Depends(get_db)):
    try:
        # Получаем пользователя по user_id
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Получаем контент из базы данных по access_level и department_id пользователя
        contents = db.query(Content).filter(
            Content.access_level == user.access_id,
            Content.department_id == user.department_id
        ).all()

        print(f"Access Level: {user.access_id}, Department ID: {user.department_id}")  # Отладочное сообщение
        print(f"Found contents: {len(contents)}")  # Количество найденного контента

        if not contents:
            raise HTTPException(status_code=404, detail="Контент не найден")

        result = []
        for content in contents:
            # Получаем название отдела
            department = db.query(Department).filter(Department.id == content.department_id).first()
            department_name = department.department_name if department else "Неизвестный отдел"
            
            # Получаем название уровня доступа
            access = db.query(Access).filter(Access.id == content.access_level).first()
            access_name = access.access_name if access else "Неизвестный уровень"
            
            result.append({
                "id": content.id,
                "title": content.title,
                "description": content.description,
                "file_path": content.file_path,
                "department_id": content.department_id,
                "department_name": department_name,
                "access_level": content.access_level,
                "access_name": access_name
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении контента: {str(e)}")

@app.get("/download-file/{content_id}")
async def download_file(content_id: int, db: Session = Depends(get_db)):
    # Получаем контент из базы данных по ID
    content = db.query(Content).filter(Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Контент не найден")

    # Проверяем, существует ли файл
    file_path = content.file_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    # Возвращаем файл как ответ
    return FileResponse(file_path, media_type='application/octet-stream', filename=os.path.basename(file_path))

@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()  # Получаем всех пользователей из базы данных
        user_list = []
        
        for user in users:
            # Получаем название отдела
            department = db.query(Department).filter(Department.id == user.department_id).first()
            department_name = department.department_name if department else "Неизвестный отдел"

            # Получаем название доступа
            access = db.query(Access).filter(Access.id == user.access_id).first()
            access_name = access.access_name if access else "Неизвестный доступ"

            user_list.append({
                "id": user.id,
                "login": user.login,
                "role_id": user.role_id,
                "department_name": department_name,
                "access_name": access_name,
            })

        return user_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении пользователей: {str(e)}")

@app.get("/api/departments")
async def get_departments(db: Session = Depends(get_db)):
    departments = db.query(Department).all()
    return [{"id": dept.id, "department_name": dept.department_name} for dept in departments]

@app.get("/api/access_levels")
async def get_access_levels(db: Session = Depends(get_db)):
    access_levels = db.query(Access).all()
    return [{"id": access_level.id, "access_name": access_level.access_name} for access_level in access_levels]

@app.put("/user/{user_id}")
async def update_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    try:
        # Получаем пользователя по ID
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Обновляем данные пользователя
        if "department_id" in user_data:
            user.department_id = user_data["department_id"]
        
        if "access_id" in user_data:
            user.access_id = user_data["access_id"]
            
        # Сохраняем изменения
        db.commit()
        db.refresh(user)
        
        return {"message": "Данные пользователя успешно обновлены"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении пользователя: {str(e)}")

@app.delete("/user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        # Получаем пользователя по ID
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Удаляем пользователя
        db.delete(user)
        db.commit()
        
        return {"message": "Пользователь успешно удален"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении пользователя: {str(e)}")

@app.put("/user/{user_id}/password")
async def update_password(user_id: int, password_data: dict, db: Session = Depends(get_db)):
    try:
        # Получаем пользователя по ID
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Хешируем новый пароль
        hashed_password = pwd_context.hash(password_data["password"])
        
        # Обновляем пароль пользователя
        user.password = hashed_password
        
        # Сохраняем изменения
        db.commit()
        
        return {"message": "Пароль пользователя успешно обновлен"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении пароля: {str(e)}")

@app.get("/departments")
async def get_departments(db: Session = Depends(get_db)):
    departments = db.query(Department).all()
    return [{"id": dept.id, "name": dept.department_name} for dept in departments]

@app.get("/access-levels")
async def get_access_level(db: Session = Depends(get_db)):
    access_levels = db.query(Access).all()
    return [{"id": access.id, "access_name": access.access_name} for access in access_levels]

if __name__ == "__main__":
    args = parse_arguments()
    main(args.model, args.embedding_model, args.path, args.web, args.port)
