from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.auth import verify_token
from app.models import User, VoiceRecord
from app.schemas import TranscriptResponse
from app.services.speech_to_text import SpeechToTextService
from app.services.text_summarizer import TextSummarizerService
from app.services.audio_storage import AudioStorageService

router = APIRouter()
security = HTTPBearer()

# Инициализируем сервисы
stt_service = SpeechToTextService()
summarizer_service = TextSummarizerService()
storage_service = AudioStorageService()


@router.post("/voice-to-text", response_model=TranscriptResponse)
async def voice_to_text(
        audio: UploadFile = File(...),
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    email = verify_token(credentials.credentials)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    audio_path = await storage_service.save_audio(audio)

    try:
        transcript = await stt_service.transcribe(audio_path)
        summary = await summarizer_service.summarize(transcript)
        voice_record = VoiceRecord(
            user_id=user.id,
            audio_path=audio_path,
            transcript=transcript,
            summary=summary,
            created_at=datetime.utcnow()
        )
        db.add(voice_record)
        db.commit()
        db.refresh(voice_record)

        return TranscriptResponse(
            id=voice_record.id,
            transcript=transcript,
            summary=summary,
            created_at=voice_record.created_at
        )

    except Exception as e:
        storage_service.delete_audio(audio_path)
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
