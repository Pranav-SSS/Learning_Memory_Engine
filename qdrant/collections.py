from qdrant_client.models import VectorParams, Distance
from qdrant.client import client
from config import VECTOR_SIZE, KNOWLEDGE_COLLECTION, MEMORY_COLLECTION

def create_collections():
    client.recreate_collection(
        collection_name=KNOWLEDGE_COLLECTION,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )

    client.recreate_collection(
        collection_name=MEMORY_COLLECTION,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )