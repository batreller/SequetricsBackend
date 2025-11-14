from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72, description="Password must be 8-72 characters")

class RegisterResponse(BaseModel):
    access_token: str
    message: str

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
