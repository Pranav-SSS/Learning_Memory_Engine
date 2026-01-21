import uuid
import math
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from qdrant.client import client
from embeddings.embed_memory import embed_memory
from memory.decay import apply_spaced_decay, update_stability
from config import MEMORY_COLLECTION, VECTOR_SIZE

def update_mastery(mastery, stability, correct):
    if correct:
        mastery += 0.15 * (1.0 - mastery) * math.log(1.0 + stability)
    else:
        mastery -= 0.2 * mastery

    return max(0.0, min(1.0, mastery))

def update_memory(student_id, concept, correct, days_passed):
    query_filter = Filter(
        must=[
            FieldCondition(key="student_id", match=MatchValue(value=student_id)),
            FieldCondition(key="concept", match=MatchValue(value=concept))
        ]
    )

    results = client.query_points(
        collection_name=MEMORY_COLLECTION,
        query=[0.0] * VECTOR_SIZE,
        with_payload=True,
        limit=1,
        query_filter=query_filter
    )

    mastery = 0.2
    stability = 2.0
    mistakes = []

    if results.points:
        payload = results.points[0].payload

        if payload is not None:
            stored_mastery = payload.get("mastery")
            stored_stability = payload.get("stability")
            stored_mistakes = payload.get("mistakes")

            mastery = apply_spaced_decay(
                stored_mastery if isinstance(stored_mastery, float) else mastery,
                days_passed,
                stored_stability if isinstance(stored_stability, float) else stability
            )

            stability = (
                stored_stability
                if isinstance(stored_stability, float)
                else stability
            )

            if isinstance(stored_mistakes, list):
                mistakes = list(stored_mistakes)

    mastery = update_mastery(mastery, stability, correct)
    stability = update_stability(stability, correct)

    if not correct:
        mistakes.append("conceptual confusion")

    vector = embed_memory(concept, mastery, mistakes)

    client.upsert(
        collection_name=MEMORY_COLLECTION,
        points=[
            PointStruct(
                id=uuid.uuid4(),
                vector=vector,
                payload={
                    "student_id": student_id,
                    "concept": concept,
                    "mastery": mastery,
                    "stability": stability,
                    "mistakes": mistakes
                }
            )
        ]
    )

    return mastery, stability