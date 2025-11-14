from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
        db: AsyncSession = Depends(get_db)
):
    email = verify_token(credentials.credentials)
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    result = await db.execute(
        select(VoiceRecord)
        .filter(VoiceRecord.user_id == user.id)
        .order_by(VoiceRecord.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    records = result.scalars().all()

    return [
        VoiceHistoryResponse(
            id=record.id,
            transcript=record.transcript,
            summary=record.summary,
            created_at=record.created_at
        )
        for record in records
    ]
