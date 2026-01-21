import json
from sentence_transformers import SentenceTransformer
from qdrant_client.models import PointStruct
from qdrant.client import client
from config import EMBEDDING_MODEL, KNOWLEDGE_COLLECTION

model = SentenceTransformer(EMBEDDING_MODEL)

def ingest_knowledge(path="data/knowledge_chunks.json"):
    with open(path) as f:
        chunks = json.load(f)
    points = []

    for chunk in chunks:
        vector = model.encode(chunk["text"]).tolist()
        points.append(
            PointStruct(
                id=chunk["id"],
                vector=vector,
                payload=chunk
            )
        )

    client.upsert(
        collection_name=KNOWLEDGE_COLLECTION,
        points=points
    )