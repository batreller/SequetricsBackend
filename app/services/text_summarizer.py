from abc import ABC, abstractmethod
from typing import List
import re
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM


class SummarizerStrategy(ABC):
    @abstractmethod
    async def summarize(self, text: str) -> str:
        pass


class BasicSummarizer(SummarizerStrategy):
    async def summarize(self, text: str) -> str:
        if len(text) <= 200:
            return text
        return text[:200] + "..."


class AirportRunwayLLMSummarizer(SummarizerStrategy):
    def __init__(self):
        model_name = "facebook/bart-large-cnn"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            use_safetensors=True
        )
        self.summarizer = pipeline(
            "summarization",
            model=self.model,
            tokenizer=self.tokenizer
        )
        # keywords for filtering important issues
        self.keywords = [
            "stripe", "stripe marking", "problem", "issue", "damage", "damaged", "crack",
            "erosion", "obstacle", "repair", "fix", "replace", "runway", "taxiway",
            "aircraft", "equipment", "maintenance", "pavement", "lighting", "signage",
            "marking", "apron", "tarmac", "groove", "incident", "obstruction",
            "foreign object", "FOD", "closure", "shutdown", "failure", "malfunction", "breakdown"
        ]

    def extract_sentences_with_keywords(self, text: str) -> List[str]:
        sentences = re.split(r'\.|\n', text)
        important_sentences = [
            s.strip() for s in sentences
            if any(keyword in s.lower() for keyword in self.keywords)
        ]
        return important_sentences

    def summarize_with_pipeline(self, text: str) -> str:
        word_count = len(text.split())

        max_len = min(200, max(50, word_count // 2))
        min_len = min(30, max_len // 3)

        summary_list = self.summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False,
            num_beams=4,
            length_penalty=1.0,
            no_repeat_ngram_size=3
        )
        summary = summary_list[0]['summary_text']
        return summary

    async def summarize(self, text: str) -> str:
        important_sentences = self.extract_sentences_with_keywords(text)
        if important_sentences:
            text_to_summarize = ". ".join(important_sentences)
        else:
            text_to_summarize = text

        summary = self.summarize_with_pipeline(text_to_summarize)
        return summary


class TextSummarizerService:
    def __init__(self, strategy: SummarizerStrategy = None):
        self.strategy = strategy or AirportRunwayLLMSummarizer()

    async def summarize(self, text: str) -> str:
        return await self.strategy.summarize(text)

    def set_strategy(self, strategy: SummarizerStrategy):
        self.strategy = strategy
