"""
Скрипт для миграции файлов из старого хранилища в новое.
Копирует все файлы в директорию /app/files/ и обновляет пути в базе данных.
"""

import os
import shutil
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append("..")  # Добавляем родительскую директорию в путь для импорта

from models_db import Content
from database import get_db, SessionLocal

def migrate_files_to_volume():
    """
    Мигрирует файлы из старого хранилища в новое (/app/files/).
    Обновляет пути в базе данных.
    """
    # Создаем директорию /app/files/, если она не существует
    os.makedirs("/app/files/", exist_ok=True)
    
    # Получаем сессию базы данных
    db = SessionLocal()
    
    try:
        # Получаем все записи с путями к файлам
        contents = db.query(Content).all()
        
        for content in contents:
            old_path = content.file_path
            
            # Пропускаем файлы, которые уже находятся в /app/files/
            if old_path.startswith('/app/files/'):
                print(f"Файл {old_path} уже в новом хранилище, пропускаем.")
                continue
            
            # Получаем имя файла из пути
            file_name = os.path.basename(old_path)
            
            # Новый путь в хранилище Docker
            new_path = f"/app/files/{file_name}"
            
            # Проверяем существует ли исходный файл
            if os.path.exists(old_path):
                try:
                    # Копируем файл в новое хранилище
                    shutil.copy2(old_path, new_path)
                    print(f"Файл скопирован: {old_path} -> {new_path}")
                    
                    # Обновляем путь в базе данных
                    content.file_path = new_path
                    db.commit()
                    print(f"Путь обновлен в БД: {old_path} -> {new_path}")
                    
                except Exception as e:
                    print(f"Ошибка при копировании файла {old_path}: {e}")
            else:
                print(f"Файл не найден: {old_path}")
                
                # Проверяем, может быть файл уже существует в новом хранилище
                if os.path.exists(new_path):
                    print(f"Файл уже существует в новом хранилище: {new_path}")
                    
                    # Обновляем путь в базе данных
                    content.file_path = new_path
                    db.commit()
                    print(f"Путь обновлен в БД: {old_path} -> {new_path}")
                else:
                    print(f"Файл не найден ни в старом, ни в новом хранилище: {file_name}")
        
        print("Миграция файлов завершена.")
    
    except Exception as e:
        print(f"Ошибка при миграции файлов: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate_files_to_volume() 