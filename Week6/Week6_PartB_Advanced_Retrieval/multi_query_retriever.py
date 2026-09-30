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


# Enable MultiQueryRetriever logging
logging.basicConfig()
logging.getLogger(
    "langchain_classic.retrievers.multi_query"
).setLevel(logging.INFO)


print("=" * 60)
print("PART B - MULTIQUERY RETRIEVER")
print("=" * 60)


# Week 5 corpus - READ ONLY
CORPUS_PATH = r"D:\Internship-Tasks\Week5\Week5_Project\data\books_corpus.json"

with open(CORPUS_PATH, "r", encoding="utf-8") as file:
    books = json.load(file)

raw_book_text = "\n\n".join(book["text"] for book in books)

print(f"Original corpus records: {len(books)}")


# Recursive text splitting
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = splitter.split_text(raw_book_text)

print(f"Generated chunks: {len(chunks)}")


# Create embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)


# Create local Chroma vector store
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
    collection_name="week6_partb_multiquery"
)


# Plain/base retriever
base_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


# Gemini model used by MultiQueryRetriever
model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0
)


# MultiQueryRetriever
retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=model
)


# Test question
question = "What is the title of the book in the library?"

print("\nQUESTION:")
print(question)

print("\nGENERATING ALTERNATIVE QUERIES...")
print("The generated queries will appear below through logging.")


# Retrieve documents using multiple generated queries
results = retriever.invoke(question)


print("\nRETRIEVED DOCUMENTS:")
print("-" * 60)

for i, document in enumerate(results, start=1):
    print(f"\nResult {i}:")
    print(document.page_content)
    print(f"Metadata: {document.metadata}")


print("\nMultiQueryRetriever completed successfully.")