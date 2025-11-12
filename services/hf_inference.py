import os
import requests
from typing import List

HF_MODEL = "jjzha/jobbert_skill_extraction"

class HFInferenceSkillExtractor:
    """Uses Hugging Face Inference API for token-classification (NER) skill extraction.

    Requires environment variable HUGGINGFACE_API_KEY to be set.
    """
    def __init__(self, model_name: str = HF_MODEL):
        self.model_name = model_name
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise RuntimeError("HUGGINGFACE_API_KEY environment variable is not set")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def extract_skills(self, text: str, min_score: float = 0.35, timeout: int = 60) -> List[str]:
        """Call the HF inference API and extract skill tokens with score filtering.

        Returns a sorted list of unique skill strings.
        """
        if not text:
            return []
        payload = {"inputs": text}
        resp = requests.post(self.api_url, headers=self.headers, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()

        skills = set()
        # data might be a list of entity dicts
        if isinstance(data, list):
            for ent in data:
                # common keys: 'word' or 'entity'/'token' and 'score' and possibly 'entity_group'
                word = ent.get("word") or ent.get("token") or ent.get("text") or ent.get("entity")
                score = ent.get("score", 0.0)
                if not word:
                    continue
                if score < min_score:
                    continue
                # normalize token artifacts
                normalized = word.replace("##", "").replace("\u0120", " ").strip()
                if normalized:
                    skills.add(normalized)

        # fallback: if API returns a dict with error or other message, return empty
        return sorted(skills)
