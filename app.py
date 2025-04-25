from langchain_ollama import ChatOllama
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from models import check_if_model_is_available
from document_loader import load_documents_into_database
import argparse
import sys

from llm import getChatChain

app = FastAPI()
chat = None
db = None
# 123123ПриёмGПАвелN
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
    
    try:
        print(f"Вызываем LLM с вопросом: {user_question}")
        response = chat(user_question)
        print(f"Ответ от LLM: {response}")  # Отладочное сообщение
        
        if response is None:
            print("Получен пустой ответ от LLM")
            raise HTTPException(status_code=500, detail="Получен пустой ответ от LLM.")
        
        # Проверяем, начинается ли ответ с "Произошла ошибка"
        if isinstance(response, str) and response.startswith("Произошла ошибка"):
            print(f"LLM вернул сообщение об ошибке: {response}")
            raise HTTPException(status_code=500, detail=response)
        
        return {"answer": response}
    except Exception as e:
        error_message = f"Ошибка при обработке запроса: {str(e)}"
        print(error_message)
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_message)

@app.post("/initialize")
async def initialize(request: InitRequest):
    success = initialize_llm(request.model_name, request.embedding_model_name, request.documents_path)
    
    if not success:
        raise HTTPException(status_code=500, detail="Не удалось инициализировать LLM.")
    return {"message": "LLM успешно инициализирован."}

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


def initialize_llm(llm_model_name: str, embedding_model_name: str, documents_path: str) -> bool:
    global chat, db
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


if __name__ == "__main__":
    args = parse_arguments()
    main(args.model, args.embedding_model, args.path, args.web, args.port)
