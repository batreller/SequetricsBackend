from abc import ABC, abstractmethod


class SummarizerStrategy(ABC):
    @abstractmethod
    async def summarize(self, text: str) -> str:
        pass


class BasicSummarizer(SummarizerStrategy):
    async def summarize(self, text: str) -> str:
        if len(text) <= 200:
            return text
        return text[:200] + "..."


class AirportRunwaySummarizer(SummarizerStrategy):
    # todo maybe add LLM

    async def summarize(self, text: str) -> str:
        keywords = ["stripe", "problem", "damage", "obstacle", "repair"]

        sentences = text.split(".")
        important_sentences = [
            s.strip() for s in sentences
            if any(keyword in s.lower() for keyword in keywords)
        ]

        if important_sentences:
            return ". ".join(important_sentences[:3]) + "."

        return text[:200] + "..." if len(text) > 200 else text


class TextSummarizerService:
    def __init__(self, strategy: SummarizerStrategy = None):
        self.strategy = strategy or AirportRunwaySummarizer()

    async def summarize(self, text: str) -> str:
        return await self.strategy.summarize(text)

    def set_strategy(self, strategy: SummarizerStrategy):
        self.strategy = strategy
