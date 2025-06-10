from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader
)
import os
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

PERSIST_DIRECTORY = "storage"
TEXT_SPLITTER = RecursiveCharacterTextSplitter(chunk_size=863, chunk_overlap=324)

def vec_search(embedding_model, query, db, n_top_cos: int = 5):
    print(f"Searching for query: {query}")
    query_emb = embedding_model.embed_documents([query])[0]
    print(f"Query embedding: {query_emb}")

    search_result = db.similarity_search_by_vector(query_emb, k=n_top_cos)
    print(f"Search results: {search_result}")

    top_chunks = [x.metadata.get('chunk') for x in search_result]
    top_files = list({x.metadata.get('file') for x in search_result if x.metadata.get('file')})

    print(f"Top chunks: {top_chunks}")
    print(f"Top files: {top_files}")

    return top_chunks, top_files

def load_documents_into_database(model_name: str, documents_path: str, department_id: str, reload: bool = True) -> Chroma:
    """
    Загружает документы из указанной директории в векторную базу данных Chroma
    после разделения текста на части, создавая базу данных для конкретного отдела.

    Args:
        model_name (str): Название модели эмбеддинга.
        documents_path (str): Путь к директории с документами.
        department_id (str): Идентификатор отдела для создания уникальной базы данных.
        reload (bool): Нужно ли перезагружать существующие документы. По умолчанию True.

    Returns:
        Chroma: Векторная база данных с загруженными документами.
    """
    # Определяем директорию для хранения данных в зависимости от отдела
    department_directory = f"{PERSIST_DIRECTORY}/{department_id}"

    # Проверяем существует ли директория для хранения данных
    if os.path.exists(department_directory) and not reload:
        print(f"Загрузка существующей базы данных Chroma для отдела {department_id}...")
        db = Chroma(
            embedding_function=OllamaEmbeddings(model=model_name),
            persist_directory=department_directory
        )
        return db
    
    # Если нужно перезагрузить документы или директория не существует
    print(f"Загрузка документов для отдела {department_id}...")
    raw_documents = load_documents(documents_path)
    
    # Если директория для хранения существует, получаем список уже загруженных файлов
    loaded_files = set()
    if os.path.exists(department_directory):
        try:
            db = Chroma(
                embedding_function=OllamaEmbeddings(model=model_name),
                persist_directory=department_directory
            )
            # Получаем список файлов, которые уже есть в базе
            all_docs = db.get()
            if all_docs and all_docs.get('metadatas'):
                for metadata in all_docs['metadatas']:
                    if metadata and 'source' in metadata:
                        loaded_files.add(metadata['source'])
            print(f"Уже загружено {len(loaded_files)} файлов")
        except Exception as e:
            print(f"Ошибка при попытке получить список загруженных файлов: {e}")
            # Если произошла ошибка, считаем что нет загруженных файлов
            loaded_files = set()
    
    # Фильтруем только новые документы
    new_documents = []
    for doc in raw_documents:
        if hasattr(doc, 'metadata') and 'source' in doc.metadata:
            if doc.metadata['source'] not in loaded_files:
                new_documents.append(doc)
        else:
            # Если у документа нет метаданных о источнике, добавляем его
            new_documents.append(doc)
    
    print(f"Найдено {len(new_documents)} новых документов из {len(raw_documents)} всего")
    
    if not new_documents:
        print("Нет новых документов для загрузки")
        # Возвращаем существующую базу данных
        if os.path.exists(department_directory):
            return Chroma(
                embedding_function=OllamaEmbeddings(model=model_name),
                persist_directory=department_directory
            )
        # Если директории нет, но и новых документов нет - создаем пустую базу
        return Chroma.from_documents(
            documents=[],
            embedding=OllamaEmbeddings(model=model_name),
            persist_directory=department_directory
        )
    
    # Разбиваем новые документы на чанки
    documents = TEXT_SPLITTER.split_documents(new_documents)
    print(f"Разбито на {len(documents)} чанков")
    
    # Создаем встраивания и загружаем в Chroma
    print("Создание встраиваний и загрузка документов в Chroma...")
    
    # Если директория существует, добавляем к существующей базе
    if os.path.exists(department_directory):
        db = Chroma(
            embedding_function=OllamaEmbeddings(model=model_name),
            persist_directory=department_directory
        )
        db.add_documents(documents)
        return db
    else:
        # Иначе создаем новую базу
        return Chroma.from_documents(
            documents=documents,
            embedding=OllamaEmbeddings(model=model_name),
            persist_directory=department_directory
        )


def load_documents(path: str) -> List[Document]:
    """
    Loads documents from the specified directory path.

    This function supports loading of PDF, Markdown, and HTML documents by utilizing
    different loaders for each file type. It checks if the provided path exists and
    raises a FileNotFoundError if it does not. It then iterates over the supported
    file types and uses the corresponding loader to load the documents into a list.

    Args:
        path (str): The path to the directory containing documents to load.

    Returns:
        List[Document]: A list of loaded documents.

    Raises:
        FileNotFoundError: If the specified path does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The specified path does not exist: {path}")

    loaders = {
        ".pdf": DirectoryLoader(
            path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True,
            use_multithreading=True,
        ),
        ".md": DirectoryLoader(
            path,
            glob="**/*.md",
            loader_cls=TextLoader,
            show_progress=True,
        ),
    }
# 
    docs = []
    for file_type, loader in loaders.items():
        print(f"Loading {file_type} files")
        docs.extend(loader.load())
    return docs

def vec_search(embedding_model, query, db, n_top_cos: int = 5):
    """
    Выполняет поиск в векторной базе Chroma: кодирует запрос и возвращает топ-фрагменты и файлы.
    """
    # Кодируем запрос в вектор
    query_emb = embedding_model.embed_documents([query])[0]

    # Поиск в базе данных
    search_result = db.similarity_search_by_vector(query_emb, k=n_top_cos)

    # Извлечение фрагментов и файлов из метаданных
    top_chunks = [x.metadata.get('chunk') for x in search_result]
    top_files = list({x.metadata.get('file') for x in search_result if x.metadata.get('file')})

    return top_chunks, top_files

def rerank_results(query: str, results: List[Document], top_k: int = 5) -> List[Tuple[Document, float]]:
    """
    Повторно ранжирует результаты на основе дополнительного анализа.

    Args:
        query (str): Исходный текст запроса.
        results (List[Document]): Список документов, полученных из векторного поиска.
        top_k (int): Количество топовых результатов для возврата.

    Returns:
        List[Tuple[Document, float]]: Список кортежей, содержащих документ и его новый ранг.
    """
    # Пример: Используем простую метрику на основе длины совпадения с запросом
    ranked_results = []
    for doc in results:
        # Пример метрики: количество совпадений слов из запроса в документе
        score = sum(1 for word in query.split() if word in doc.page_content)
        ranked_results.append((doc, score))
    
    # Сортируем результаты по убыванию ранга
    ranked_results.sort(key=lambda x: x[1], reverse=True)
    
    # Возвращаем топовые результаты
    return ranked_results[:top_k]

# Пример использования
# results = vec_search(embedding_model, query, db, n_top_cos=10)
# reranked_results = rerank_results(query, results)
