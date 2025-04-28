from langchain_ollama import ChatOllama, OllamaEmbeddings
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import optuna

from models import check_if_model_is_available
from document_loader import load_documents_into_database, vec_search
import argparse
import sys

from llm import getChatChain

# Инициализация глобальных переменных
app = FastAPI()
chat = None
db = None
embedding_model = None
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

@app.post("/optimize")
async def optimize():
    try:
        # Запуск оптимизации
        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=100)  # Укажите количество испытаний

        # Возврат лучших гиперпараметров
        return {"best_hyperparameters": study.best_params}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

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


# Функция цели для оптимизации
def objective(trial):
    # Определите гиперпараметры, которые вы хотите оптимизировать
    embedding_model_name = trial.suggest_categorical("embedding_model_name", ["nomic-embed-text", "another-model"])
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-5, 1e-1)
    batch_size = trial.suggest_int("batch_size", 1, 32)
    chunk_size = trial.suggest_int("chunk_size", 100, 2000)
    chunk_overlap = trial.suggest_int("chunk_overlap", 50, 600)
    n_top_cos = trial.suggest_int("n_top_cos", 1, 8)

    # Загрузите документы и инициализируйте модель
    db = load_documents_into_database(embedding_model_name, "Research")
    llm = ChatOllama(model=embedding_model_name)

    # Здесь вы можете обучить модель и оценить её производительность
    accuracy = train_and_evaluate_model(llm, db, learning_rate, batch_size, chunk_size, chunk_overlap, n_top_cos)

    return accuracy  # Возвращаем значение, которое нужно максимизировать

def train_and_evaluate_model(llm, db, learning_rate, batch_size, chunk_size, chunk_overlap, n_top_cos):
    """
    Обучает модель и оценивает её производительность.

    Args:
        llm: Модель для обучения.
        db: База данных для получения данных.
        learning_rate: Скорость обучения.
        batch_size: Размер пакета для обучения.
        chunk_size: Размер чанка для обработки.
        chunk_overlap: Перекрытие чанков.
        n_top_cos: Количество топовых результатов для поиска.

    Returns:
        float: Точность модели на валидационном наборе данных.
    """
    # Здесь должна быть логика обучения модели
    # Например, вы можете использовать данные из базы данных для обучения

    # Пример: просто возвращаем случайное значение для имитации точности
    import random
    accuracy = random.uniform(0.5, 1.0)  # Имитация точности
    return accuracy


if __name__ == "__main__":
    args = parse_arguments()
    main(args.model, args.embedding_model, args.path, args.web, args.port)


