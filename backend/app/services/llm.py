from langchain_ollama import ChatOllama, OllamaEmbeddings
from fastapi import HTTPException
from app.db.models import ChatHistory
from app.services.document_loader import vec_search
from sqlalchemy.orm import Session

def getChatChain(llm, db):
    """
    Создает функцию для обработки запросов к LLM с использованием RAG
    """
    def chat_func(user_question):
        try:
            # Выполняем векторный поиск для получения релевантных фрагментов
            chunks, files = vec_search(OllamaEmbeddings(model=llm.model), user_question, db)
            
            # Формируем контекст из найденных фрагментов
            context = "\n\n".join(chunks)
            
            # Формируем запрос к LLM с контекстом
            prompt = f"""Ответь на вопрос, используя следующий контекст:
            
            Контекст:
            {context}
            
            Вопрос: {user_question}
            
            Ответ:"""
            
            # Получаем ответ от LLM
            response = llm.invoke(prompt)
            
            # Извлекаем текст ответа
            if hasattr(response, "content"):
                answer = response.content
            else:
                answer = str(response)
                
            # Сохраняем историю чата в базу данных
            chat_history = ChatHistory(
                user_message=user_question,
                assistant_message=answer,
                model=llm.model
            )
            db.add(chat_history)
            db.commit()
            
            return answer
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при обработке запроса: {str(e)}")
    
    return chat_func

def process_query(question: str, model: str, db: Session) -> dict:
    """
    Обрабатывает запрос пользователя и возвращает ответ
    """
    try:
        # Создаем экземпляр модели
        llm = ChatOllama(model=model)
        
        # Получаем функцию чата
        chat = getChatChain(llm, db)
        
        # Выполняем векторный поиск
        chunks, files = vec_search(OllamaEmbeddings(model=model), question, db)
        
        # Получаем ответ от модели
        answer = chat(question)
        
        return {"answer": answer, "chunks": chunks, "files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def initialize(model_name: str, embedding_model_name: str, documents_path: str, db: Session) -> bool:
    """
    Инициализирует LLM и загружает документы в базу данных
    """
    try:
        # Проверяем доступность модели
        # Примечание: здесь должен быть импорт check_if_model_is_available из models.py
        # и вызов этой функции для проверки доступности модели
        
        # Загружаем документы в базу данных
        # Этот шаг должен быть реализован в document_loader.py
        
        return True
    except Exception as e:
        print(f"Ошибка при инициализации: {str(e)}")
        return False 