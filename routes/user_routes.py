from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
import secrets
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
import os

from sqlalchemy.orm import Session
from database import get_db
from models_db import Access, Content, User, Department
from pydantic import BaseModel

router = APIRouter(prefix="/user", tags=["user"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    login: str
    password: str
    role_id: int
    department_id: int
    access_id: int

@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Проверка существования пользователя
    existing_user = db.query(User).filter(User.login == user.login).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    # Хеширование пароля
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        login=user.login,
        password=hashed_password,
        role_id=user.role_id,
        department_id=user.department_id,
        access_id=user.access_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Пользователь успешно зарегистрирован"}

class UserLogin(BaseModel):
    login: str
    password: str

def generate_auth_key() -> str:
    """Генерация случайного ключа аутентификации."""
    return secrets.token_hex(16)

@router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == user_data.login).first()
    if not user or not user.check_password(user_data.password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    auth_key = generate_auth_key()
    user.auth_key = auth_key
    db.commit()
    
    return {
        "id": user.id,
        "login": user.login,
        "auth_key": auth_key,
        "role_id": user.role_id,
        "department_id": user.department_id,
        "access_id": user.access_id
    }


@router.get("/user/{id}")
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Получаем название отдела
    department = db.query(Department).filter(Department.id == user.department_id).first()
    department_name = department.department_name if department else "Неизвестный отдел"

    # Получаем название доступа
    access = db.query(Access).filter(Access.id == user.access_id).first()
    access_name = access.access_name if access else "Неизвестный доступ"

    return {
        "login": user.login,
        "role_id": user.role_id,
        "department_name": department_name,
        "access_name": access_name,
    }

@router.get("/user/{user_id}/content")
async def get_user_content(user_id: int, db: Session = Depends(get_db)):
    try:
        # Получаем пользователя по user_id
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Получаем контент из базы данных по access_level и department_id пользователя
        contents = db.query(Content).filter(
            Content.access_level == user.access_id,
            Content.department_id == user.department_id
        ).all()

        print(f"Access Level: {user.access_id}, Department ID: {user.department_id}")  # Отладочное сообщение
        print(f"Found contents: {len(contents)}")  # Количество найденного контента

        if not contents:
            raise HTTPException(status_code=404, detail="Контент не найден")

        result = []
        for content in contents:
            # Получаем название отдела
            department = db.query(Department).filter(Department.id == content.department_id).first()
            department_name = department.department_name if department else "Неизвестный отдел"
            
            # Получаем название уровня доступа
            access = db.query(Access).filter(Access.id == content.access_level).first()
            access_name = access.access_name if access else "Неизвестный уровень"
            
            result.append({
                "id": content.id,
                "title": content.title,
                "description": content.description,
                "file_path": content.file_path,
                "department_id": content.department_id,
                "department_name": department_name,
                "access_level": content.access_level,
                "access_name": access_name
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении контента: {str(e)}")


@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()  # Получаем всех пользователей из базы данных
        user_list = []
        
        for user in users:
            # Получаем название отдела
            department = db.query(Department).filter(Department.id == user.department_id).first()
            department_name = department.department_name if department else "Неизвестный отдел"

            # Получаем название доступа
            access = db.query(Access).filter(Access.id == user.access_id).first()
            access_name = access.access_name if access else "Неизвестный доступ"

            user_list.append({
                "id": user.id,
                "login": user.login,
                "role_id": user.role_id,
                "department_name": department_name,
                "access_name": access_name,
            })

        return user_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении пользователей: {str(e)}")


@router.put("/user/{user_id}")
async def update_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    try:
        # Получаем пользователя по ID
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Обновляем данные пользователя
        if "department_id" in user_data:
            user.department_id = user_data["department_id"]
        
        if "access_id" in user_data:
            user.access_id = user_data["access_id"]
            
        # Сохраняем изменения
        db.commit()
        db.refresh(user)
        
        return {"message": "Данные пользователя успешно обновлены"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении пользователя: {str(e)}")

@router.delete("/user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        # Получаем пользователя по ID
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Удаляем пользователя
        db.delete(user)
        db.commit()
        
        return {"message": "Пользователь успешно удален"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении пользователя: {str(e)}")

@router.put("/user/{user_id}/password")
async def update_password(user_id: int, password_data: dict, db: Session = Depends(get_db)):
    try:
        # Получаем пользователя по ID
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Хешируем новый пароль
        hashed_password = pwd_context.hash(password_data["password"])
        
        # Обновляем пароль пользователя
        user.password = hashed_password
        
        # Сохраняем изменения
        db.commit()
        
        return {"message": "Пароль пользователя успешно обновлен"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении пароля: {str(e)}")
