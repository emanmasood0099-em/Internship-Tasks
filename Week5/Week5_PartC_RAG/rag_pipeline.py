import os
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(
    name="library_rag",
    configuration={
        "embedding_function": None
    }
)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def embed(text: str) -> list[float]:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return result.embeddings[0].values


def add_document(text: str, source: str):
    chunks = chunk_text(text)

    embeddings = [embed(chunk) for chunk in chunks]

    collection.add(
        documents=chunks,
        metadatas=[
            {"source": source, "chunk": i}
            for i in range(len(chunks))
        ],
        ids=[
            f"{source}-{i}"
            for i in range(len(chunks))
        ],
        embeddings=embeddings
    )


def retrieve(question: str, k: int = 3):
    question_embedding = embed(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=k
    )

    return results["documents"][0], results["metadatas"][0]


# Document 1
add_document(
    """
    The Solar System contains the Sun and the objects that orbit it.
    The eight planets are Mercury, Venus, Earth, Mars, Jupiter, Saturn,
    Uranus, and Neptune.

    Earth is the third planet from the Sun. It has liquid water on its
    surface and supports a wide variety of life. The Moon is Earth's
    natural satellite and orbits around Earth.
    """,
    "space.txt"
)


# Document 2
add_document(
    """
    Python is a popular programming language used in web development,
    automation, data analysis, artificial intelligence, and machine learning.

    Python uses simple and readable syntax. It supports important concepts
    such as variables, functions, loops, conditions, lists, and dictionaries.
    """,
    "python.txt"
)


# Document 3
add_document(
    """
    The Amazon rainforest is located mainly in South America.
    It is one of the most biologically diverse regions on Earth.

    The rainforest contains millions of plants, animals, and insects.
    It also plays an important role in the global carbon cycle and climate.
    """,
    "rainforest.txt"
)


# Document 4
add_document(
    """
    Basketball is a team sport played by two teams.
    Each team tries to score points by putting the ball through the
    opponent's basket.

    Players commonly perform skills such as dribbling, passing, shooting,
    and rebounding. Teamwork and coordination are important parts of the game.
    """,
    "basketball.txt"
)


# Task 1 confirmation
print("4 documents added successfully.")


# Task 4 - Question and Retrieval
question = "Which planet is third from the Sun?"

chunks, metadata = retrieve(question)

print("Question:", question)

print("\nRetrieved Chunks:")

for chunk, meta in zip(chunks, metadata):
    print("\nSource:", meta["source"])
    print("Chunk:", meta["chunk"])
    print("Text:", chunk)


# Generate final answer
context = "\n\n".join(chunks)

prompt = f"""
Answer the question using ONLY the provided context.

If the answer is not contained in the context, do not make up an answer.
Instead, say exactly:

I don't have that information in the provided documents.

Context:
{context}

Question:
{question}

Answer:
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print("\nFinal Answer:")
print(response.text)


# Task 4 - Source Attribution
print("\nSources:")

for meta in metadata:
    print(f"- {meta['source']} (Chunk {meta['chunk']})")