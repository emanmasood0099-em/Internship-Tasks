import json
import logging

from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)
from langchain_classic.retrievers.multi_query import MultiQueryRetriever


# Load environment variables
load_dotenv()

# Show generated MultiQuery queries
logging.basicConfig()
logging.getLogger(
    "langchain_classic.retrievers.multi_query"
).setLevel(logging.INFO)


print("=" * 70)
print("PART B - PLAIN RETRIEVER VS MULTIQUERY RETRIEVER")
print("=" * 70)


# Week 5 corpus - READ ONLY
CORPUS_PATH = r"D:\Internship-Tasks\Week5\Week5_Project\data\books_corpus.json"

with open(CORPUS_PATH, "r", encoding="utf-8") as file:
    books = json.load(file)

raw_book_text = "\n\n".join(book["text"] for book in books)


# Recursive splitting
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = splitter.split_text(raw_book_text)


# Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)


# Vector store
vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings,
    metadatas=[
        {
            "source": "week5_books_corpus",
            "chunk_id": i + 1
        }
        for i in range(len(chunks))
    ],
    collection_name="week6_partb_comparison"
)


# Plain retriever
plain_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


# Gemini model for MultiQueryRetriever
model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0
)


# MultiQueryRetriever
multiquery_retriever = MultiQueryRetriever.from_llm(
    retriever=plain_retriever,
    llm=model
)


# Same 5 questions from Week 5 manual RAG evaluation
questions = [
    "Which planet is third from the Sun?",
    "What programming language is used for web development, automation, and artificial intelligence?",
    "Where is the Amazon rainforest located mainly?",
    "What skills are commonly used in basketball?",
    "What is the capital of Japan?"
]


# Run all questions
for number, question in enumerate(questions, start=1):

    print("\n")
    print("=" * 70)
    print(f"QUESTION {number}")
    print("=" * 70)
    print(question)

    # Plain retrieval
    plain_results = plain_retriever.invoke(question)

    print("\n--- PLAIN RETRIEVER RESULTS ---")

    if plain_results:
        for i, document in enumerate(plain_results, start=1):
            print(f"Result {i}:")
            print(document.page_content)
    else:
        print("No documents retrieved.")

    # MultiQuery retrieval
    print("\n--- MULTIQUERY RETRIEVER RESULTS ---")

    multi_results = multiquery_retriever.invoke(question)

    if multi_results:
        for i, document in enumerate(multi_results, start=1):
            print(f"Result {i}:")
            print(document.page_content)
    else:
        print("No documents retrieved.")


print("\n")
print("=" * 70)
print("5-QUESTION COMPARISON COMPLETED")
print("=" * 70)