from fastapi import APIRouter, HTTPException
import os
import shutil

router = APIRouter(prefix="/directory", tags=["directory"])

@router.post("/create")
async def create_directory(directory_path: str):
    """
    Создает директорию по указанному пути.
    
    Args:
        directory_path (str): Путь к директории, которую нужно создать.
    
    Returns:
        dict: Сообщение об успешном создании директории.
    """
    try:
        # Проверяем, начинается ли путь с /app/files/
        if not directory_path.startswith('/app/files/'):
            # Если нет, добавляем префикс
            full_path = f"/app/files/{directory_path}"
        else:
            full_path = directory_path
            
        # Проверяем, существует ли директория
        if not os.path.exists(full_path):
            os.makedirs(full_path)  # Создаем директорию
            return {"message": f"Директория '{full_path}' успешно создана."}
        else:
            return {"message": f"Директория '{full_path}' уже существует."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete")
async def delete_directory(directory_path: str):
    """
    Удаляет директорию по указанному пути.
    
    Args:
        directory_path (str): Путь к директории, которую нужно удалить.
    
    Returns:
        dict: Сообщение об успешном удалении директории.
    """
    try:
        # Проверяем, начинается ли путь с /app/files/
        if not directory_path.startswith('/app/files/'):
            # Если нет, добавляем префикс
            full_path = f"/app/files/{directory_path}"
        else:
            full_path = directory_path
            
        # Проверяем, существует ли директория
        if os.path.exists(full_path):
            shutil.rmtree(full_path)  # Удаляем директорию и её содержимое
            return {"message": f"Директория '{full_path}' успешно удалена."}
        else:
            raise HTTPException(status_code=404, detail=f"Директория '{full_path}' не найдена.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_directory(directory_path: str = "/app/files"):
    """
    Возвращает список файлов и директорий по указанному пути.
    
    Args:
        directory_path (str): Путь к директории, содержимое которой нужно получить.
    
    Returns:
        dict: Список файлов и директорий.
    """
    try:
        # Проверяем, начинается ли путь с /app/files/
        if not directory_path.startswith('/app/files'):
            # Если нет, добавляем префикс
            full_path = f"/app/files/{directory_path}"
        else:
            full_path = directory_path
            
        # Проверяем, существует ли директория
        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail=f"Директория '{full_path}' не найдена.")
            
        # Получаем список файлов и директорий
        items = os.listdir(full_path)
        
        # Разделяем на файлы и директории
        directories = []
        files = []
        
        for item in items:
            item_path = os.path.join(full_path, item)
            if os.path.isdir(item_path):
                directories.append(item)
            else:
                files.append(item)
                
        return {
            "path": full_path,
            "directories": directories,
            "files": files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))