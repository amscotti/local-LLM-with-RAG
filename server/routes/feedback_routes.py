from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Form
import os
from sqlalchemy.orm import Session
from database import get_db
from models_db import Feedback, User
from pydantic import BaseModel
from fastapi.responses import FileResponse, Response
from typing import List, Optional
import base64
from io import BytesIO

router = APIRouter(prefix="/feedback", tags=["feedback"])

class FeedbackCreate(BaseModel):
    user_id: int
    text: str

@router.post("/create")
async def create_feedback(
    user_id: int = Form(...),
    text: str = Form(...),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Создает новое сообщение обратной связи с возможностью прикрепления фото
    """
    try:
        # Проверяем существование пользователя
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Обрабатываем фото, если оно предоставлено
        photo_data = None
        if photo:
            photo_data = await photo.read()
        
        # Создаем новую запись обратной связи
        new_feedback = Feedback(
            user_id=user_id,
            text=text,
            photo=photo_data
        )
        
        # Сохраняем в базу данных
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        
        return {"message": "Сообщение обратной связи успешно создано", "feedback_id": new_feedback.id}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании сообщения: {str(e)}")

@router.get("/list")
async def get_feedback_list(db: Session = Depends(get_db)):
    """
    Получает список всех сообщений обратной связи (доступно только для администраторов)
    """
    try:
        # В реальном приложении здесь должна быть проверка прав администратора
        # if not current_user.is_admin:
        #     raise HTTPException(status_code=403, detail="Доступ запрещен")
        
        # Получаем все сообщения обратной связи
        feedback_list = db.query(Feedback).order_by(Feedback.created_at.desc()).all()
        
        # Формируем ответ
        result = []
        for feedback in feedback_list:
            # Получаем информацию о пользователе
            user = db.query(User).filter(User.id == feedback.user_id).first()
            user_info = {
                "id": user.id,
                "login": user.login,
                "full_name": user.full_name
            } if user else {"id": feedback.user_id, "login": "Неизвестно", "full_name": "Неизвестно"}
            
            # Добавляем информацию о сообщении
            result.append({
                "id": feedback.id,
                "text": feedback.text,
                "created_at": feedback.created_at,
                "has_photo": feedback.photo is not None,
                "user": user_info
            })
        
        return {"feedback_list": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении списка сообщений: {str(e)}")

@router.get("/photo/{feedback_id}")
async def get_feedback_photo(feedback_id: int, db: Session = Depends(get_db)):
    """
    Получает фото для сообщения обратной связи по его ID
    """
    try:
        # В реальном приложении здесь должна быть проверка прав администратора
        # if not current_user.is_admin:
        #     raise HTTPException(status_code=403, detail="Доступ запрещен")
        
        # Находим сообщение по ID
        feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        if not feedback:
            raise HTTPException(status_code=404, detail="Сообщение не найдено")
        
        # Проверяем наличие фото
        if not feedback.photo:
            raise HTTPException(status_code=404, detail="Фото не найдено")
        
        # Возвращаем фото
        return Response(content=feedback.photo, media_type="image/jpeg")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении фото: {str(e)}")

@router.get("/detail/{feedback_id}")
async def get_feedback_detail(feedback_id: int, db: Session = Depends(get_db)):
    """
    Получает детальную информацию о сообщении обратной связи по его ID
    """
    try:
        # В реальном приложении здесь должна быть проверка прав администратора
        # if not current_user.is_admin:
        #     raise HTTPException(status_code=403, detail="Доступ запрещен")
        
        # Находим сообщение по ID
        feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        if not feedback:
            raise HTTPException(status_code=404, detail="Сообщение не найдено")
        
        # Получаем информацию о пользователе
        user = db.query(User).filter(User.id == feedback.user_id).first()
        user_info = {
            "id": user.id,
            "login": user.login,
            "full_name": user.full_name,
            "department_id": user.department_id,
            "access_id": user.access_id
        } if user else {"id": feedback.user_id, "login": "Неизвестно", "full_name": "Неизвестно"}
        
        # Формируем ответ
        result = {
            "id": feedback.id,
            "text": feedback.text,
            "created_at": feedback.created_at,
            "has_photo": feedback.photo is not None,
            "user": user_info
        }
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении информации о сообщении: {str(e)}")
