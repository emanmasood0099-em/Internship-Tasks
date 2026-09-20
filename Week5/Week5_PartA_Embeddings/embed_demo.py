import os
import numpy as np
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def embed(text: str) -> list[float]:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values


def cosine_similarity(a, b) -> float:
    a, b = np.array(a), np.array(b)

    return float(
        np.dot(a, b) /
        (np.linalg.norm(a) * np.linalg.norm(b))
    )


v1 = embed("A young wizard attends a magic school")
v2 = embed("A boy learns spells at an academy")
v3 = embed("A recipe for chocolate cake")

print("similar meaning:", cosine_similarity(v1, v2))
print("unrelated meaning:", cosine_similarity(v1, v3))
print("embedding length:", len(v1))


v4 = embed("I loved this book")
v5 = embed("I did not love this book")

print("opposite meaning:", cosine_similarity(v4, v5))