from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Form
import os
from sqlalchemy.orm import Session
from database import get_db
from models_db import Access, Content, User, Tag
from pydantic import BaseModel
from fastapi.responses import FileResponse
from typing import List


router = APIRouter(prefix="/content", tags=["content"])

# Эндпоинт для загрузки файлов
@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    # Проверка на уникальность имени файла
    if file.filename in os.listdir("Research"):  # Предполагается, что "Research" - это папка для хранения файлов
        return {"message": "Файл с таким именем уже существует."}

    # Сохранение файла
    file_location = f"Research/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    return {"message": f"Файл '{file.filename}' успешно загружен."}

@router.post("/upload-content")
async def upload_content(
    title: str,
    description: str,
    access_id: int,
    department_id: int,
    directory_path: str,
    file: UploadFile = File(...),
    tag_id: int = None,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    # Создаем директорию, если она не существует
    os.makedirs(directory_path, exist_ok=True)
    
    # Заменяем обратные слэши на прямые для совместимости с Linux
    directory_path = directory_path.replace('\\', '/')
    
    # Сохранение файла на сервере в указанной директории
    file_location = f"{directory_path}/{file.filename}"  # Используем указанный путь
    
    # with open(file_location, "wb") as f:
    #     f.write(await file.read())


    try:
        with open(file_location, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении файла: {str(e)}")

    # Проверка существования уровня доступа
    access = db.query(Access).filter(Access.id == access_id).first()
    if access is None:
        raise HTTPException(status_code=400, detail="Уровень доступа не найден")

    # Создание записи в базе данных
    new_content = Content(
        title=title,
        description=description,
        file_path=file_location,
        access_level=access_id,
        department_id=department_id,
        tag_id=tag_id  # Указываем тег, если он есть
    )
    db.add(new_content)
    db.commit()
    db.refresh(new_content)

    return {"message": "Контент успешно загружен"}

@router.post("/upload-files")
async def upload_files(
    files: List[UploadFile] = File(...),
    directory_path: str = Form(...),
    db: Session = Depends(get_db)
):
    # Создаем директорию, если она не существует
    os.makedirs(directory_path, exist_ok=True);
    
    # Список для хранения информации о загруженных файлах
    uploaded_files_info = [];

    for file in files:
        # Сохранение файла на сервере в указанной директории
        file_location = f"{directory_path}/{file.filename}";
        
        try:
            with open(file_location, "wb") as f:
                f.write(await file.read());
            
            # Добавление информации о файле в базу данных
            new_content = Content(
                title=file.filename,
                description="Загруженный файл",
                file_path=file_location,
                access_level=1,  # Уровень доступа по умолчанию, можно изменить
                department_id=1,  # ID отдела по умолчанию, можно изменить
                tag_id=None  # Можно добавить тег, если нужно
            );
            db.add(new_content);
            db.commit();
            db.refresh(new_content);

            uploaded_files_info.append({
                "filename": file.filename,
                "file_path": file_location
            });
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при сохранении файла {file.filename}: {str(e)}");

    return {"message": "Файлы успешно загружены", "files": uploaded_files_info};

# Модель для обновления контента
class ContentUpdate(BaseModel):
    title: str = None
    description: str = None
    access_id: int = None
    department_id: int = None
    tag_id: int = None

@router.put("/{content_id}")
async def update_content(
    content_id: int,
    content_data: ContentUpdate,
    db: Session = Depends(get_db)
):
    # Отладочный вывод входных параметров
    print(f"Получены параметры: content_id={content_id}, data={content_data}")
    
    # Получаем контент из базы данных по ID
    content = db.query(Content).filter(Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Контент не найден")

    # Обновляем поля, если они были переданы
    if content_data.title is not None:
        content.title = content_data.title
    if content_data.description is not None:
        content.description = content_data.description
    if content_data.access_id is not None:
        # Проверка существования уровня доступа
        access = db.query(Access).filter(Access.id == content_data.access_id).first()
        if access is None:
            raise HTTPException(status_code=400, detail="Уровень доступа не найден")
        content.access_level = content_data.access_id
    if content_data.department_id is not None:
        content.department_id = content_data.department_id
    if content_data.tag_id is not None:
        content.tag_id = content_data.tag_id

    db.commit()
    db.refresh(content)

    return {"message": "Контент успешно обновлен", "content": content}

class ContentBase(BaseModel):
    id: int
    title: str
    description: str
    file_path: str

    class Config:
        orm_mode = True

@router.get("/content/filter")
async def get_content_by_access_and_department(
    access_level: int,
    department_id: int,
    tag_id: int = None,  # Новый параметр для фильтрации по тегу
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Content).filter(
            Content.access_level == access_level,
            Content.department_id == department_id
        )
        
        if tag_id is not None:
            query = query.filter(Content.tag_id == tag_id)  # Фильтрация по тегу

        contents = query.all()

        if not contents:
            raise HTTPException(status_code=404, detail="Контент не найден")

        return [
            {
                "id": content.id,
                "title": content.title,
                "description": content.description,
                "file_path": content.file_path,
                "access_level": content.access_level,
                "department_id": content.department_id,
                "tag_id": content.tag_id  # Возвращаем ID тега
            } for content in contents
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении контента: {str(e)}")
    
    
@router.get("/content/{content_id}")
async def get_content_by_id(content_id: int, db: Session = Depends(get_db)):
    try:
        content = db.query(Content).filter(Content.id == content_id).first()
        if content is None:
            raise HTTPException(status_code=404, detail="Контент не найден")
        
        return {
            "id": content.id,
            "title": content.title,
            "description": content.description,
            "file_path": content.file_path,
            "access_level": content.access_level,
            "department_id": content.department_id,
            "tag_id": content.tag_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении контента: {str(e)}")

@router.delete("/content/{content_id}")
async def delete_content(content_id: int, db: Session = Depends(get_db)):
    try:
        # Получаем контент по ID
        content = db.query(Content).filter(Content.id == content_id).first()
        if not content:
            raise HTTPException(status_code=404, detail="Контент не найден")
        
        # Сохраняем путь к файлу
        file_path = content.file_path
        
        # Удаляем контент из базы данных
        db.delete(content)
        db.commit()
        
        # Удаляем файл с сервера, если он существует
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Ошибка при удалении файла {file_path}: {e}")
        
        return {"message": "Контент успешно удален"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении контента: {str(e)}")


@router.get("/all")
async def get_all_content(db: Session = Depends(get_db)):
    try:
        contents = db.query(Content).all()
        return [
            {
                "id": content.id,
                "title": content.title,
                "description": content.description,
                "file_path": content.file_path,
                "access_level": content.access_level,
                "department_id": content.department_id,
                "tag_id": content.tag_id
            } for content in contents
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении контента: {str(e)}")
    
    
@router.get("/download-file/{content_id}")
async def download_file(content_id: int, db: Session = Depends(get_db)):
    # Получаем контент из базы данных по ID
    content = db.query(Content).filter(Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Контент не найден")

    # Проверяем, существует ли файл
    file_path = content.file_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    # Возвращаем файл как ответ
    return FileResponse(file_path, media_type='application/octet-stream', filename=os.path.basename(file_path))

@router.get("/view-file/{content_id}")
async def view_file(content_id: int, db: Session = Depends(get_db)):
    # Получаем контент из базы данных по ID
    content = db.query(Content).filter(Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Контент не найден")

    # Проверяем, существует ли файл
    file_path = content.file_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    # Определяем тип файла на основе расширения
    file_extension = os.path.splitext(file_path)[1].lower()
    
    # Устанавливаем соответствующий media_type в зависимости от расширения файла
    if file_extension in ['.pdf']:
        media_type = 'application/pdf'
    elif file_extension in ['.mp3', '.wav', '.ogg']:
        media_type = f'audio/{file_extension[1:]}'
    elif file_extension in ['.mp4', '.webm', '.avi', '.mov']:
        media_type = f'video/{file_extension[1:]}'
    elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
        media_type = f'image/{file_extension[1:]}'
    else:
        # Для других типов файлов используем общий тип
        media_type = 'application/octet-stream'

    # Возвращаем файл как ответ с заголовком для открытия в браузере
    return FileResponse(file_path, media_type=media_type, filename=os.path.basename(file_path), headers={"Content-Disposition": "inline"})

@router.get("/user/{user_id}/content/by-tags/{tag_id}")
async def get_user_content_by_tags_and_tag_id(user_id: int, tag_id: int, db: Session = Depends(get_db)):
    try:
        # Получаем пользователя по user_id
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Получаем контент для данного тега с учетом прав доступа пользователя
        tag_content = db.query(Content).filter(
            Content.tag_id == tag_id,
            Content.access_level == user.access_id,
            Content.department_id == user.department_id
        ).all()
        
        if not tag_content:
            raise HTTPException(status_code=404, detail="Контент не найден")

        return [
            {
                "id": content.id,
                "title": content.title,
                "description": content.description,
                "file_path": content.file_path
            }
            for content in tag_content
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении контента: {str(e)}")

@router.get("/search-documents")
async def search_documents(
    user_id: int,
    search_query: str = None,
    db: Session = Depends(get_db)
):
    try:
        # Получаем пользователя по user_id для проверки прав доступа
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Базовый запрос с учетом прав доступа пользователя
        query = db.query(Content).filter(
            Content.access_level == user.access_id,
            Content.department_id == user.department_id
        )
        
        # Если указан поисковый запрос, добавляем условия поиска
        if search_query:
            from sqlalchemy import or_
            # Поиск по названию, описанию или пути файла
            query = query.filter(
                or_(
                    Content.title.ilike(f"%{search_query}%"),  # Поиск по названию
                    Content.description.ilike(f"%{search_query}%"),  # Поиск по описанию
                    Content.file_path.ilike(f"%{search_query}%")  # Поиск по пути файла (включая имя файла)
                )
            )
        
        # Выполняем запрос
        contents = query.all()
        
        # Формируем результат
        documents = [
            {
                "id": content.id,
                "title": content.title,
                "description": content.description,
                "file_path": content.file_path,
                "tag_id": content.tag_id
            }
            for content in contents
        ]
        
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при поиске документов: {str(e)}")

@router.post("/create-tag")
async def create_tag(tag_name: str, db: Session = Depends(get_db)):
    try:
        new_tag = Tag(tag_name=tag_name)
        db.add(new_tag)
        db.commit()
        db.refresh(new_tag)
        return {"message": "Тег успешно создан", "tag": new_tag}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании тега: {str(e)}")

@router.put("/update-tag/{tag_id}")
async def update_tag(tag_id: int, tag_name: str, db: Session = Depends(get_db)):
    try:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if tag is None:
            raise HTTPException(status_code=404, detail="Тег не найден")
        tag.tag_name = tag_name
        db.commit()
        db.refresh(tag)
        return {"message": "Тег успешно обновлен", "tag": tag}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении тега: {str(e)}")

@router.delete("/delete-tag/{tag_id}")
async def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    try:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if tag is None: 
            raise HTTPException(status_code=404, detail="Тег не найден")
        db.delete(tag)
        db.commit()
        return {"message": "Тег успешно удален"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении тега: {str(e)}") 