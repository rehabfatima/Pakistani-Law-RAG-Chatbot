def create_prompt(question, context):
    return f"""
You are a Pakistani law assistant.
Answer only using the legal context below.
Do not invent legal information.
If the answer is not in the context, say so clearly.

Legal Context:
{context}

Question:
{question}

Answer:
"""
