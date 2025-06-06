from langchain_ollama import ChatOllama, OllamaEmbeddings
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel
import uvicorn
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

from models_db import User, Department, Access
from document_loader import load_documents_into_database, vec_search
import argparse
import sys
from database import get_db

from llm import getChatChain

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
    success = initialize_llm(request.model_name, request.embedding_model_name, request.documents_path)
    
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

def initialize_llm(llm_model_name: str, embedding_model_name: str, documents_path: str) -> bool:
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
        db = load_documents_into_database(embedding_model_name, documents_path)
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

@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    # Отладочное сообщение для проверки входящих данных
    print("Полученные данные для входа:", user)

    db_user = db.query(User).filter(User.login == user.login).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    print("Полученные данные для входа:", user)

    return {"message": "Успешная авторизация"}
    print("Полученные данные для входа:", user)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)

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




if __name__ == "__main__":
    args = parse_arguments()
    main(args.model, args.embedding_model, args.path, args.web, args.port)
