from abc import ABC, abstractmethod
import whisper
import torch
from app.config import settings


class STTStrategy(ABC):
    @abstractmethod
    async def transcribe(self, audio_path: str) -> str:
        pass


class WhisperSTT(STTStrategy):
    def __init__(self):
        # todo use logger
        device = "cuda" if settings.USE_GPU and torch.cuda.is_available() else "cpu"
        print(f"Loading Whisper model '{settings.WHISPER_MODEL}' on device: {device}")
        self.model = whisper.load_model(settings.WHISPER_MODEL, device=device)

    async def transcribe(self, audio_path: str) -> str:
        result = self.model.transcribe(audio_path, language="ru")
        return result["text"]


class SpeechToTextService:
    def __init__(self, strategy: STTStrategy = None):
        self.strategy = strategy or WhisperSTT()

    async def transcribe(self, audio_path: str) -> str:
        return await self.strategy.transcribe(audio_path)

    def set_strategy(self, strategy: STTStrategy):
        self.strategy = strategy
