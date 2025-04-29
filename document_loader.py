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

def load_documents_into_database(model_name: str, documents_path: str, reload: bool = True) -> Chroma:
    """
    Loads documents from the specified directory into the Chroma database
    after splitting the text into chunks.

    Returns:
        Chroma: The Chroma database with loaded documents.
    """

    if reload:
        print("Loading documents")
        raw_documents = load_documents(documents_path)
        documents = TEXT_SPLITTER.split_documents(raw_documents)

        print("Creating embeddings and loading documents into Chroma")
        return Chroma.from_documents(
            documents=documents,
            embedding=OllamaEmbeddings(model=model_name),
            persist_directory=PERSIST_DIRECTORY
        )
    else:
        return Chroma(
            embedding_function=OllamaEmbeddings(model=model_name),
            persist_directory=PERSIST_DIRECTORY
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
