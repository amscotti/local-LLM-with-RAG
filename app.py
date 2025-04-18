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

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query(request: QueryRequest):
    global chat
    if chat is None:
        raise HTTPException(status_code=500, detail="LLM не инициализирован. Запустите сервер с правильными параметрами.")
    
    user_question = request.question
    response = chat(user_question)
    return response

def initialize_llm(llm_model_name: str, embedding_model_name: str, documents_path: str) -> bool:
    global chat, db
    # Check to see if the models available, if not attempt to pull them
    try:
        check_if_model_is_available(llm_model_name)
        check_if_model_is_available(embedding_model_name)
    except Exception as e:
        print(e)
        return False

    # Creating database form documents
    try:
        db = load_documents_into_database(embedding_model_name, documents_path)
    except FileNotFoundError as e:
        print(e)
        return False

    llm = ChatOllama(model=llm_model_name)
    chat = getChatChain(llm, db)
    return True

def main(llm_model_name: str, embedding_model_name: str, documents_path: str, web_mode: bool = False, port: int = 8000) -> None:
    success = initialize_llm(llm_model_name, embedding_model_name, documents_path)
    
    if not success:
        sys.exit(1)
    
    if web_mode:
        print(f"Запуск HTTP сервера на порту {port}...")
        uvicorn.run(app, host="0.0.0.0", port=port)
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
