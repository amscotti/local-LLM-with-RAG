from fastapi import UploadFile, HTTPException
import os
import json
import numpy as np
from langchain_ollama import OllamaEmbeddings
from app.db.models import Document, DocumentChunk
from sqlalchemy.orm import Session
import shutil

def load_documents_into_database(embedding_model_name: str, documents_path: str, db: Session) -> object:
    """
    Загружает документы из указанной директории в базу данных
    и создает векторные эмбеддинги для каждого фрагмента
    
    Args:
        embedding_model_name (str): Название модели для эмбеддингов
        documents_path (str): Путь к директории с документами
        db (Session): Сессия базы данных
        
    Returns:
        object: Объект базы данных
    """
    try:
        # Проверяем существование директории
        if not os.path.exists(documents_path):
            os.makedirs(documents_path)
            print(f"Создана директория {documents_path}")
            return db
            
        # Получаем список файлов в директории
        files = [f for f in os.listdir(documents_path) if os.path.isfile(os.path.join(documents_path, f))]
        
        if not files:
            print(f"В директории {documents_path} нет файлов")
            return db
            
        # Инициализируем модель эмбеддингов
        embedding_model = OllamaEmbeddings(model=embedding_model_name)
        
        # Обрабатываем каждый файл
        for file_name in files:
            file_path = os.path.join(documents_path, file_name)
            
            # Проверяем, есть ли уже этот документ в базе
            existing_doc = db.query(Document).filter(Document.path == file_path).first()
            if existing_doc:
                print(f"Документ {file_name} уже загружен, пропускаем")
                continue
                
            # Читаем содержимое файла
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Создаем запись документа
            document = Document(
                title=file_name,
                path=file_path,
                content=content
            )
            db.add(document)
            db.flush()  # Получаем ID документа
            
            # Разбиваем документ на фрагменты (чанки)
            # Здесь можно использовать более сложную логику разбиения
            chunks = split_text(content)
            
            # Создаем эмбеддинги для каждого фрагмента
            for chunk_text in chunks:
                if not chunk_text.strip():
                    continue
                    
                # Получаем эмбеддинг для фрагмента
                embedding = embedding_model.embed_query(chunk_text)
                
                # Сохраняем эмбеддинг как JSON строку
                embedding_json = json.dumps(embedding)
                
                # Создаем запись фрагмента
                chunk = DocumentChunk(
                    document_id=document.id,
                    content=chunk_text,
                    embedding=embedding_json
                )
                db.add(chunk)
                
        # Сохраняем изменения в базе данных
        db.commit()
        print(f"Загружено {len(files)} документов")
        
        return db
    except Exception as e:
        db.rollback()
        print(f"Ошибка при загрузке документов: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def vec_search(embedding_model, user_question, db, n_top_cos=5):
    """
    Выполняет векторный поиск по базе данных
    
    Args:
        embedding_model: Модель для создания эмбеддингов
        user_question (str): Вопрос пользователя
        db (Session): Сессия базы данных
        n_top_cos (int): Количество фрагментов для возврата
        
    Returns:
        tuple: (список фрагментов, список файлов)
    """
    try:
        # Получаем эмбеддинг для вопроса пользователя
        question_embedding = embedding_model.embed_query(user_question)
        
        # Получаем все фрагменты из базы данных
        chunks = db.query(DocumentChunk).all()
        
        if not chunks:
            return [], []
            
        # Вычисляем косинусное сходство для каждого фрагмента
        similarities = []
        for chunk in chunks:
            # Преобразуем строку JSON в список
            chunk_embedding = json.loads(chunk.embedding)
            
            # Вычисляем косинусное сходство
            similarity = cosine_similarity(question_embedding, chunk_embedding)
            similarities.append((chunk, similarity))
            
        # Сортируем по убыванию сходства
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Берем top-n фрагментов
        top_chunks = [chunk[0].content for chunk in similarities[:n_top_cos]]
        
        # Получаем соответствующие документы
        top_chunk_ids = [chunk[0].document_id for chunk in similarities[:n_top_cos]]
        top_docs = db.query(Document).filter(Document.id.in_(top_chunk_ids)).all()
        top_files = [doc.title for doc in top_docs]
        
        return top_chunks, top_files
    except Exception as e:
        print(f"Ошибка при векторном поиске: {str(e)}")
        return [], []

def save_uploaded_file(file: UploadFile, db: Session) -> dict:
    """
    Сохраняет загруженный файл в директорию Research и обновляет базу данных
    
    Args:
        file (UploadFile): Загруженный файл
        db (Session): Сессия базы данных
        
    Returns:
        dict: Сообщение о результате операции
    """
    try:
        # Создаем директорию Research, если она не существует
        research_dir = "Research"
        if not os.path.exists(research_dir):
            os.makedirs(research_dir)
            
        # Путь для сохранения файла
        file_path = os.path.join(research_dir, file.filename)
        
        # Проверяем, существует ли уже файл с таким именем
        existing_doc = db.query(Document).filter(Document.path == file_path).first()
        if existing_doc:
            return {"message": f"Файл с именем '{file.filename}' уже существует."}
            
        # Сохраняем файл
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Загружаем файл в базу данных
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Создаем запись документа
        document = Document(
            title=file.filename,
            path=file_path,
            content=content
        )
        db.add(document)
        db.commit()
        
        return {"message": f"Файл '{file.filename}' успешно загружен."}
    except Exception as e:
        db.rollback()
        print(f"Ошибка при загрузке файла: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def split_text(text, chunk_size=1000, overlap=200):
    """
    Разбивает текст на фрагменты
    
    Args:
        text (str): Исходный текст
        chunk_size (int): Размер фрагмента в символах
        overlap (int): Размер перекрытия между фрагментами
        
    Returns:
        list: Список фрагментов
    """
    if not text:
        return []
        
    chunks = []
    i = 0
    text_len = len(text)
    
    while i < text_len:
        # Вычисляем конец фрагмента
        end = min(i + chunk_size, text_len)
        
        # Если это не последний фрагмент, находим конец предложения
        if end < text_len:
            # Ищем ближайшую точку, вопросительный или восклицательный знак
            for j in range(end, max(i, end - 100), -1):
                if j < text_len and text[j] in ['.', '?', '!', '\n']:
                    end = j + 1
                    break
                    
        # Добавляем фрагмент
        chunks.append(text[i:end])
        
        # Перемещаем начало с учетом перекрытия
        i = end - overlap
        if i < 0:
            i = 0
            
    return chunks

def cosine_similarity(v1, v2):
    """
    Вычисляет косинусное сходство между двумя векторами
    
    Args:
        v1 (list): Первый вектор
        v2 (list): Второй вектор
        
    Returns:
        float: Косинусное сходство
    """
    v1 = np.array(v1)
    v2 = np.array(v2)
    
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    if norm_v1 == 0 or norm_v2 == 0:
        return 0
        
    return dot_product / (norm_v1 * norm_v2) 