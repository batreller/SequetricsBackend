from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class TranscriptResponse(BaseModel):
    id: int
    transcript: str
    summary: Optional[str]
    created_at: datetime


class VoiceHistoryResponse(BaseModel):
    id: int
    transcript: str
    summary: Optional[str]
    created_at: datetime
