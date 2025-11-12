from typing import List, Set
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

MODEL_NAME = "jjzha/jobbert_skill_extraction"

class HFSkillExtractor:
    """Simple wrapper around a Hugging Face token-classification model to extract skills.

    This is synchronous (blocking). Use it via asyncio.to_thread from async code.
    """
    def __init__(self, model_name: str = MODEL_NAME, device: int = -1):
        # device=-1 uses CPU; device=0 would use GPU
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        # pipeline with aggregation to merge tokens into complete entities
        try:
            self.ner = pipeline(
                "ner",
                model=self.model,
                tokenizer=self.tokenizer,
                aggregation_strategy="simple",
                device=device,
            )
        except TypeError:
            # older transformers versions use aggregation_strategy name 'grouped_entities'
            self.ner = pipeline(
                "ner",
                model=self.model,
                tokenizer=self.tokenizer,
                grouped_entities=True,
                device=device,
            )

    def _chunk_text(self, text: str, approx_max_chars: int = 1800) -> List[str]:
        """Chunk long text into roughly sized pieces to avoid tokenizer truncation.

        A rough heuristic; better chunking can be implemented if needed.
        """
        if not text:
            return []
        text = text.strip()
        if len(text) <= approx_max_chars:
            return [text]
        chunks: List[str] = []
        start = 0
        while start < len(text):
            end = start + approx_max_chars
            if end < len(text):
                # try not to cut words
                last_space = text.rfind(" ", start, end)
                if last_space > start:
                    end = last_space
            chunks.append(text[start:end].strip())
            start = end
        return chunks

    def extract_skills(self, text: str, min_score: float = 0.35) -> List[str]:
        """Extract and deduplicate skill phrases from `text`.

        Returns a sorted list for deterministic ordering.
        """
        if not text or not text.strip():
            return []

        skills: Set[str] = set()
        chunks = self._chunk_text(text)
        for chunk in chunks:
            try:
                entities = self.ner(chunk)
            except Exception:
                # if a chunk fails, skip it
                continue
            # entities come as dicts with keys like 'entity_group' and 'word' and 'score'
            for ent in entities:
                score = ent.get("score", 0.0)
                word = ent.get("word") or ent.get("entity") or ""
                label = ent.get("entity_group") or ent.get("entity")
                if not word:
                    continue
                if score < min_score:
                    continue
                # normalize subword artifacts
                normalized = word.replace("##", "").replace("\u0120", " ").strip()
                if normalized:
                    skills.add(normalized)

        return sorted(skills)
