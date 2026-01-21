from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def embed_memory(concept, mastery, mistakes):
    text = (
        f"Concept: {concept}. "
        f"Mastery: {mastery}. "
        f"Mistakes: {', '.join(mistakes) if mistakes else 'none'}."
    )
    return model.encode(text).tolist()