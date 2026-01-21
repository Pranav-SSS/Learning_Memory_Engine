from qdrant.collections import create_collections
from embeddings.embed_knowledge import ingest_knowledge
from demo.simulate_student import simulate
from demo.demo_query import run_demo_query

def main():
    create_collections()
    ingest_knowledge()

    student_id = "S123"
    simulate(student_id)

    run_demo_query(
        student_id=student_id,
        query="Why does a book remain at rest on a table?",
        concept="Newton First Law"
    )

if __name__ == "__main__":
    main()