import json
import os

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Load environment variables
load_dotenv()

# Week 5 corpus is READ-ONLY. We do not modify it.
CORPUS_PATH = r"D:\Internship-Tasks\Week5\Week5_Project\data\books_corpus.json"


def load_corpus():
    """Load the existing Week 5 corpus without modifying it."""
    with open(CORPUS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def create_chunks():
    """Create chunks using RecursiveCharacterTextSplitter."""
    corpus = load_corpus()

    raw_text = "\n\n".join(item["text"] for item in corpus)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_text(raw_text)

    return chunks


if __name__ == "__main__":
    chunks = create_chunks()

    print("=" * 60)
    print("PART B - RECURSIVE CHARACTER TEXT SPLITTER")
    print("=" * 60)

    print(f"Original corpus records: {len(load_corpus())}")
    print(f"Generated chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print(chunk)

    print("\nRecursive splitting completed successfully.")