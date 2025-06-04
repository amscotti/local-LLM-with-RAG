from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.services import llm_service, document_service
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    model: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    chunks: List[str]
    files: List[str]

class InitRequest(BaseModel):
    model_name: Optional[str] = settings.DEFAULT_LLM_MODEL
    embedding_model_name: Optional[str] = settings.DEFAULT_EMBEDDING_MODEL
    documents_path: Optional[str] = settings.DOCUMENTS_PATH

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest, db: Session = Depends(get_db)):
    try:
        response = llm_service.process_query(
            request.question, 
            request.model or settings.DEFAULT_LLM_MODEL, 
            db
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/initialize")
async def initialize(request: InitRequest, db: Session = Depends(get_db)):
    try:
        success = llm_service.initialize(
            request.model_name,
            request.embedding_model_name,
            request.documents_path,
            db
        )
        if not success:
            raise HTTPException(status_code=500, detail="Не удалось инициализировать LLM.")
        return {"message": "LLM успешно инициализирован."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        result = document_service.save_uploaded_file(file, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
