def build_prompt(query, memory_summary, docs):
    context = "\n".join(
        f"- {d.payload['concept']}: {d.payload['text']}"
        for d in docs if d.payload
    )

    return f"""
Student Memory:
{memory_summary}

Use ONLY the information below.

Retrieved Content:
{context}

Question:
{query}
"""