import os

import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI
from google import genai
from pydantic import BaseModel

from rag_pipeline import get_embedding


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="Library Knowledge Assistant")

CHROMA_PATH = "chroma_db"


class AskRequest(BaseModel):
    question: str


def get_collection():
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    return chroma_client.get_or_create_collection(
        name="library_knowledge",
        embedding_function=None
    )


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/ask")
def ask(request: AskRequest):
    collection = get_collection()

    query_embedding = get_embedding(request.question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n".join(documents)

    prompt = f"""
You are a Library Knowledge Assistant.

Answer the user's question ONLY using the provided library context.

If the answer is not available in the context, say exactly:
I don't have that information in the provided documents.

Library Context:
{context}

User Question:
{request.question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    answer = response.text.strip()

    sources = []

    for metadata in metadatas:
        title = metadata.get("title")

        if title and title not in sources:
            sources.append(title)

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }
