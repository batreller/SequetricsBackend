import os
import aiofiles
from fastapi import UploadFile
from app.config import settings
import uuid


class AudioStorageService:
    def __init__(self):
        os.makedirs(settings.AUDIO_STORAGE_PATH, exist_ok=True)

    async def save_audio(self, audio: UploadFile) -> str:
        file_extension = audio.filename.split(".")[-1] if "." in audio.filename else "mp3"
        filename = f"{uuid.uuid4()}.{file_extension}"
        filepath = os.path.join(settings.AUDIO_STORAGE_PATH, filename)

        async with aiofiles.open(filepath, 'wb') as f:
            content = await audio.read()
            await f.write(content)

        return filepath

    def delete_audio(self, audio_path: str):
        if os.path.exists(audio_path):
            os.remove(audio_path)
