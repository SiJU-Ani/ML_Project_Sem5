import os
import requests
import math
from typing import List

# Use Hugging Face Inference API for embeddings to avoid heavy local installs.
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class SemanticSimilarity:
    def __init__(self, model_name: str = DEFAULT_EMBEDDING_MODEL):
        self.model_name = model_name
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise RuntimeError("HUGGINGFACE_API_KEY is required for HF inference embeddings")
        self.url = "https://api-inference.huggingface.co/embeddings"
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        payload = {"model": self.model_name, "input": texts}
        resp = requests.post(self.url, headers=self.headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        # Expecting {'data': [{'embedding': [...]}, ...]} or list of embeddings
        if isinstance(data, dict) and "data" in data:
            embeddings = [item.get("embedding") for item in data["data"]]
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and "embedding" in data[0]:
            embeddings = [item.get("embedding") for item in data]
        elif isinstance(data, list) and all(isinstance(x, list) for x in data):
            embeddings = data
        else:
            raise RuntimeError("Unexpected embeddings response shape from Hugging Face API")
        return embeddings

    def similarity(self, a: str, b: str) -> float:
        """Return cosine similarity (0-100) between two texts using HF embeddings."""
        if not a or not b:
            return 0.0
        embs = self._get_embeddings([a, b])
        v0, v1 = embs[0], embs[1]
        # cosine similarity
        denom = math.sqrt(sum(x * x for x in v0)) * math.sqrt(sum(x * x for x in v1))
        if denom == 0:
            return 0.0
        dot = sum(x * y for x, y in zip(v0, v1))
        sim = dot / denom
        return float(sim) * 100.0

