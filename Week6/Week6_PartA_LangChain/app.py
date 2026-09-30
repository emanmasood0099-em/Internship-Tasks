import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from google import genai

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables
load_dotenv()


# Gemini client for embeddings
gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Existing Week 5 Chroma database
CHROMA_PATH = Path(
    r"D:\Internship-Tasks\Week5\Week5_Project\chroma_db"
)

COLLECTION_NAME = "library_knowledge"


# Connect to existing Chroma collection
chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = chroma_client.get_collection(
    COLLECTION_NAME
)


def get_embedding(text: str):
    """
    Generate the same type of embedding used in Week 5.
    """
    result = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return result.embeddings[0].values


def retrieve_documents(question: str):
    """
    Retrieve the most relevant documents from
    the existing Week 5 Chroma collection.
    """
    query_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    documents = results["documents"][0]

    return documents


def format_docs(docs) -> str:
    """
    Convert retrieved documents into one context string.
    """
    return "\n\n".join(docs)


def guard_short_questions(inputs: dict) -> dict:
    """
    Reject questions shorter than 3 characters.
    """
    question = inputs["question"].strip()

    if len(question) < 3:
        raise ValueError(
            "Question too short to answer meaningfully."
        )

    return inputs


# Gemini chat model
model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0
)


# Prompt
prompt = ChatPromptTemplate.from_template(
    """
You are a Library Knowledge Assistant.

Answer the user's question ONLY using the provided library context.

If the answer is not available in the context, say:
I don't have that information in the provided documents.

Library Context:
{context}

User Question:
{question}

Answer:
"""
)


# LCEL chain
chain = (
    RunnableLambda(guard_short_questions)
    | {
        "context": (
            RunnableLambda(lambda x: x["question"])
            | RunnableLambda(retrieve_documents)
            | RunnableLambda(format_docs)
        ),
        "question": RunnablePassthrough()
    }
    | RunnableLambda(
        lambda x: {
            "context": x["context"],
            "question": x["question"]["question"]
        }
    )
    | prompt
    | model
    | StrOutputParser()
)


if __name__ == "__main__":

    question = "What is the title of the book in the library?"

    print("QUESTION:")
    print(question)

    print("\nANSWER:")

    answer = chain.invoke(
        {
            "question": question
        }
    )

    print(answer)