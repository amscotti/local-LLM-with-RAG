from operator import itemgetter

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.messages import get_buffer_string
from langchain_core.prompts import format_document
from langchain.prompts.prompt import PromptTemplate


condense_question = """Задача: Переформулируй вопрос пользователя, сделав его самостоятельным и понятным без контекста предыдущего разговора.

### История разговора:
{chat_history}

### Новый вопрос пользователя:
{question}

### Переформулированный самостоятельный вопрос:
Исходя из контекста беседы, пользователь спрашивает:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(condense_question)

answer = """
### Инструкция:
Ты — профессиональный ассистент, который помогает пользователям найти точную информацию в корпоративных документах.

### Правила работы:
1. ВСЕГДА сначала внимательно изучи предоставленные документы
2. Если информация есть в документах — используй ТОЛЬКО её для ответа
3. Если информации нет в документах — честно скажи об этом
4. Давай подробные и структурированные ответы
5. При цитировании указывай источник документа

### Контекст из документов:
{context}

### Вопрос пользователя:
{question}

### Ответ:
Проанализировав предоставленные документы:"""
ANSWER_PROMPT = ChatPromptTemplate.from_template(answer)

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(
    template="📄 Источник: {source} (страница {page})\n📝 Содержание:\n{page_content}\n"
)


def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n" + "="*50 + "\n"
):
    """Улучшенная функция объединения документов с лучшим форматированием"""
    if not docs:
        return "Документы не найдены или недоступны."
    
    doc_strings = []
    for i, doc in enumerate(docs, 1):
        try:
            # Проверяем наличие метаданных
            source = "Неизвестный источник"
            page = "Неизвестно"
            
            if hasattr(doc, 'metadata') and doc.metadata:
                source = doc.metadata.get('source', source)
                page = doc.metadata.get('page', page)
            
            # Формируем контент с заголовком
            content = f"📄 Документ {i}\n"
            content += f"📁 Файл: {source}\n"
            content += f"📄 Страница: {page}\n"
            content += f"📝 Содержание:\n{doc.page_content}\n"
            
            doc_strings.append(content)
        except Exception as e:
            print(f"Ошибка при обработке документа {i}: {e}")
            doc_strings.append(f"📄 Документ {i}: Ошибка обработки")
    
    result = document_separator.join(doc_strings)
    print(f"Объединено {len(doc_strings)} документов в контекст размером {len(result)} символов")
    return result


def getStreamingChain(question: str, memory, llm, db):
    retriever = db.as_retriever(search_kwargs={"k": 10})
    loaded_memory = RunnablePassthrough.assign(
        chat_history=RunnableLambda(
            lambda x: "\n".join(
                [f"{item['role']}: {item['content']}" for item in x["memory"]]
            )
        ),
    )

    standalone_question = {
        "standalone_question": {
            "question": lambda x: x["question"],
            "chat_history": lambda x: x["chat_history"],
        }
        | CONDENSE_QUESTION_PROMPT
        | llm
        | (lambda x: x.content if hasattr(x, "content") else x)
    }

    retrieved_documents = {
        "docs": itemgetter("standalone_question") | retriever,
        "question": lambda x: x["standalone_question"],
    }

    final_inputs = {
        "context": lambda x: _combine_documents(x["docs"]),
        "question": itemgetter("question"),
    }

    answer = final_inputs | ANSWER_PROMPT | llm

    final_chain = loaded_memory | standalone_question | retrieved_documents | answer

    return final_chain.stream({"question": question, "memory": memory})


def getChatChain(llm, db):
    # Улучшенные настройки retriever для лучшего качества RAG
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 15,  # Увеличиваем количество документов
        }
    )

    def chat(question: str):
        # Инициализация памяти для каждого запроса
        memory = ConversationBufferMemory(return_messages=True, output_key="answer", input_key="question")
        
        loaded_memory = RunnablePassthrough.assign(
            chat_history=RunnableLambda(memory.load_memory_variables)
            | itemgetter("history"),
        )

        standalone_question = {
            "standalone_question": {
                "question": lambda x: x["question"],
                "chat_history": lambda x: get_buffer_string(x["chat_history"]),
            }
            | CONDENSE_QUESTION_PROMPT
            | llm
            | (lambda x: x.content if hasattr(x, "content") else x)
        }

        # Теперь мы извлекаем документы
        retrieved_documents = {
            "docs": itemgetter("standalone_question") | retriever,
            "question": lambda x: x["standalone_question"],
        }

        # Теперь мы строим входные данные для финального запроса
        final_inputs = {
            "context": lambda x: _combine_documents(x["docs"]),
            "question": itemgetter("question"),
        }

        # И, наконец, мы делаем часть, которая возвращает ответы
        answer = {
            "answer": final_inputs
            | ANSWER_PROMPT
            | llm.with_config(callbacks=[StreamingStdOutCallbackHandler()]),
            "docs": itemgetter("docs"),
        }

        final_chain = loaded_memory | standalone_question | retrieved_documents | answer

        try:
            print(f"getChatChain: обработка вопроса: {question}")
            inputs = {"question": question}
            result = final_chain.invoke(inputs)
            
            if "answer" not in result:
                print("getChatChain: ключ 'answer' отсутствует в результате")
                return "Не удалось получить ответ от модели"
                
            answer_content = result["answer"].content if hasattr(result["answer"], "content") else result["answer"]
            memory.save_context(inputs, {"answer": answer_content})
            
            print(f"getChatChain: успешный ответ: {answer_content[:100]}...")
            return answer_content
        except Exception as e:
            import traceback
            print(f"getChatChain: ошибка при обработке вопроса: {str(e)}")
            print(traceback.format_exc())
            return f"Произошла ошибка при обработке запроса: {str(e)}"

    return chat
