from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import llm
from app.core.config import settings
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db

app = FastAPI(title=settings.PROJECT_NAME)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене замените на список конкретных доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавление маршрутов API
app.include_router(llm.router, prefix=settings.API_V1_STR + "/llm")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/check-db")
def check_db(db: Session = Depends(get_db)):
    try:
        # Используйте text() для выполнения SQL выражения
        db.execute(text("SELECT 1"))
        return {"status": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка подключения к БД: {str(e)}")
# http://127.0.0.1:8000/docs   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
