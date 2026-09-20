import json
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

CORPUS_FILE = Path("data/books_corpus.json")
CHROMA_PATH = "chroma_db"


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def get_embedding(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return result.embeddings[0].values


def load_corpus():
    with open(CORPUS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_collection():
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    return chroma_client.get_or_create_collection(
        name="library_knowledge",
        embedding_function=None
    )


def store_chunks(collection):
    documents = load_corpus()

    total_chunks = 0

    for document in documents:
        chunks = chunk_text(document["text"])

        for index, chunk in enumerate(chunks):
            chunk_id = f"{document['id']}_chunk_{index}"

            embedding = get_embedding(chunk)

            collection.upsert(
                ids=[chunk_id],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{
                    "title": document["metadata"]["title"],
                    "author_id": str(document["metadata"]["author_id"]),
                    "category_id": str(document["metadata"]["category_id"])
                }]
            )

            total_chunks += 1

    return total_chunks


def retrieve(question, collection, k=3):
    query_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results


if __name__ == "__main__":
    collection = get_collection()

    total_chunks = store_chunks(collection)

    print(f"Books loaded: {len(load_corpus())}")
    print(f"Chunks stored: {total_chunks}")
    print("Chroma collection: library_knowledge")

    question = "What is the title of the book in the library?"

    results = retrieve(question, collection)

    print("\nQUESTION:")
    print(question)

    print("\nRETRIEVED DOCUMENTS:")

    for document, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        print(f"- {document}")
        print(f"  Title: {metadata['title']}")
        print(f"  Category ID: {metadata['category_id']}")