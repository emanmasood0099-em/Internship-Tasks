import json
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# Load environment variables
load_dotenv()

print("=" * 60)
print("PART B - PLAIN RETRIEVER")
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
    collection_name="week6_partb_plain_retriever"
)


# Convert vector store into a Retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


# Test question
question = "What is the title of the book in the library?"

print("\nQUESTION:")
print(question)

# Retrieve relevant chunks
results = retriever.invoke(question)

print("\nRETRIEVED DOCUMENTS:")
print("-" * 60)

for i, document in enumerate(results, start=1):
    print(f"\nResult {i}:")
    print(document.page_content)
    print(f"Metadata: {document.metadata}")


print("\nPlain retriever completed successfully.")