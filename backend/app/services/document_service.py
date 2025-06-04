from fastapi import UploadFile
from app.db.database import get_db

def save_uploaded_file(file: UploadFile, db) -> dict:
    # Логика для сохранения загруженного файла
    return {"message": f"Файл '{file.filename}' успешно загружен."}
