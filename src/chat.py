from src.clients import get_oai_client
from src.retrieval import search


oai_client = get_oai_client()

context = ""

def ask(question: str, document_id: str = ""):
    context = search(
        search_text=question,
        document_id=document_id,
        top=5,
    )

    response = oai_client.chat.completions.create(
        model="gpt-5.4-mini",  
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
Answer the user's question using the provided context.
If the answer cannot be found in the context, say so.
""",
            },
            {
                "role": "user",
                "content": f"""
Context:

{context}

Question:

{question}
""",
            },
        ],
    )

    return response.choices[0].message.content

def chat(question: str, context: str):
    response = oai_client.chat.completions.create(
        model="gpt-5.4-mini",  
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """
Answer the user's question using the provided context.
If the answer cannot be found in the context, say so.
""",
            },
            {
                "role": "user",
                "content": f"""
Context:

{context}

Question:

{question}
""",
            },
        ],
    )

    return response.choices[0].message.content
