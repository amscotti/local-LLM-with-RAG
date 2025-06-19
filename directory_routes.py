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
        # Проверяем, существует ли директория
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)  # Создаем директорию
            return {"message": f"Директория '{directory_path}' успешно создана."}
        else:
            raise HTTPException(status_code=400, detail=f"Директория '{directory_path}' уже существует.")
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
        # Проверяем, существует ли директория
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)  # Удаляем директорию и её содержимое
            return {"message": f"Директория '{directory_path}' успешно удалена."}
        else:
            raise HTTPException(status_code=404, detail=f"Директория '{directory_path}' не найдена.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))