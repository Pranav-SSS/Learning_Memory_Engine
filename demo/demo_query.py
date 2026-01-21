from sentence_transformers import SentenceTransformer
from rl.policy import TeachingPolicy
from retrieval.retriever import retrieve_knowledge
from retrieval.retrieval_policy import decide_policy
from reasoning.prompt_builder import build_prompt
from reasoning.response_generator import generate_response
from qdrant.client import client
from qdrant_client.models import Filter, FieldCondition, MatchValue
from config import EMBEDDING_MODEL, MEMORY_COLLECTION, VECTOR_SIZE

policy = TeachingPolicy()

def run_demo_query(student_id, query, concept):
    model = SentenceTransformer(EMBEDDING_MODEL)
    query_vector = model.encode(query).tolist()

    memory_filter = Filter(
        must=[
            FieldCondition(
                key="student_id",
                match=MatchValue(value=student_id)
            ),
            FieldCondition(
                key="concept",
                match=MatchValue(value=concept)
            )
        ]
    )

    memory_results = client.query_points(
        collection_name=MEMORY_COLLECTION,
        query=[0.0] * VECTOR_SIZE,
        with_payload=True,
        limit=1,
        query_filter=memory_filter
    )

    mastery = 0.2
    stability = 2.0

    if memory_results.points:
        payload = memory_results.points[0].payload

        if payload is not None:
            stored_mastery = payload.get("mastery")
            stored_stability = payload.get("stability")

            if isinstance(stored_mastery, float):
                mastery = stored_mastery

            if isinstance(stored_stability, float):
                stability = stored_stability

    state = (round(mastery, 1), int(stability))
    action = policy.select_action(state)

    difficulty, limit = decide_policy(mastery)
    docs = retrieve_knowledge(query_vector, difficulty, limit)

    memory_summary = (
        f"Mastery={mastery}, "
        f"Stability={stability}, "
        f"RL_Action={action}"
    )

    prompt = build_prompt(query, memory_summary, docs)
    answer = generate_response(prompt)

    print("\n==== DEMO QUERY ====\n")
    print("Student query:", query)
    print("Current mastery:", mastery)
    print("Current stability:", stability)
    print("RL-chosen teaching strategy:", action)

    print("\n==== GENERATED ANSWER ====\n")
    print(answer)

    print("\n==== RECOMMENDATION ====\n")
    print("Next step: Practice simple real-life examples before advancing.")