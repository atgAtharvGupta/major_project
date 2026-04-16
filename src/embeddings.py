import numpy as np
from sentence_transformers import SentenceTransformer

from src.config import EMBEDDING_MODEL, HF_TOKEN


_MODEL = None


def get_model():
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    try:
        # Newer SentenceTransformers uses `token` instead of `use_auth_token`.
        _MODEL = SentenceTransformer(EMBEDDING_MODEL, token=HF_TOKEN if HF_TOKEN else None)
    except Exception as e:
        print(f"Warning: could not load embedding model {EMBEDDING_MODEL}. Error: {e}")
        _MODEL = False
    return _MODEL

def get_embedding(text: str) -> list[float]:
    """Returns the embedding vector for the text."""
    if not text:
        return []
    model = get_model()
    if not model:
        return []
    embeddings = model.encode([text], normalize_embeddings=True)
    return embeddings[0].tolist()

def compute_similarity(text1: str, text2: str) -> float:
    """Computes cosine similarity between two texts."""
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    if not emb1 or not emb2:
        return 0.0
        
    vec1 = np.array(emb1)
    vec2 = np.array(emb2)
    
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return float(dot / (norm1 * norm2))
