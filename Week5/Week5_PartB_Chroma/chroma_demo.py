import os
import numpy as np
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def embed(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return float(
        np.dot(a, b) /
        (np.linalg.norm(a) * np.linalg.norm(b))
    )


chroma_client = chromadb.Client()

collection = chroma_client.create_collection(
    name="books_demo",
    configuration={
        "embedding_function": None
    }
)

documents = [
    "A young wizard attends a magic school and fights a dark lord.",
    "A crew travels through a wormhole to save humanity from a dying Earth.",
    "Two feuding families in 19th century England navigate love and marriage.",
    "A detective investigates a mysterious murder in a small town.",
    "A group of astronauts explores a distant planet.",
]

metadatas = [
    {"source": "book_1.txt", "category": "Fantasy"},
    {"source": "book_2.txt", "category": "Science Fiction"},
    {"source": "book_3.txt", "category": "Romance"},
    {"source": "book_4.txt", "category": "Mystery"},
    {"source": "book_5.txt", "category": "Science Fiction"},
]

ids = [
    "book_1",
    "book_2",
    "book_3",
    "book_4",
    "book_5"
]

embeddings = [embed(document) for document in documents]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
    embeddings=embeddings
)

query = "a space journey story"
query_embedding = embed(query)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

print("Query:", query)
print("Documents:")
print(results["documents"])
print("Metadata:")
print(results["metadatas"])