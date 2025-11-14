from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import verify_token
from app.models import User, VoiceRecord
from app.schemas import VoiceHistoryResponse

router = APIRouter()
security = HTTPBearer()


@router.get("/history", response_model=List[VoiceHistoryResponse])
async def get_history(
        limit: int = 5,
        offset: int = 0,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    email = verify_token(credentials.credentials)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    records = db.query(VoiceRecord) \
        .filter(VoiceRecord.user_id == user.id) \
        .order_by(VoiceRecord.created_at.desc()) \
        .offset(offset) \
        .limit(limit) \
        .all()

    return [
        VoiceHistoryResponse(
            id=record.id,
            transcript=record.transcript,
            summary=record.summary,
            created_at=record.created_at
        )
        for record in records
    ]
