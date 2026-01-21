from qdrant_client.models import Filter, FieldCondition, MatchValue
from qdrant.client import client
from config import KNOWLEDGE_COLLECTION

def retrieve_knowledge(query_vector, difficulty, limit):
    query_filter = Filter(
        must=[
            FieldCondition(
                key="difficulty",
                match=MatchValue(value=difficulty)
            )
        ]
    )

    results = client.query_points(
        collection_name=KNOWLEDGE_COLLECTION,
        query=query_vector,
        with_payload=True,
        limit=limit,
        query_filter=query_filter
    )

    return results.points