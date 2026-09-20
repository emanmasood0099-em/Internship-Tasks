import json
import requests
from pathlib import Path

API_URL = "http://localhost:5032/api/books"
OUTPUT_FILE = Path("data/books_corpus.json")


def fetch_books():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()


def build_corpus(books):
    documents = []

    for book in books:
        title = book.get("title", "Unknown Title")
        author_id = book.get("authorId", "Unknown Author")
        category_id = book.get("categoryId", "Unknown Category")

        text = (
            f"Book Title: {title}. "
            f"Author ID: {author_id}. "
            f"Category ID: {category_id}."
        )

        documents.append({
            "id": f"book_{book.get('bookId')}",
            "text": text,
            "metadata": {
                "title": title,
                "author_id": author_id,
                "category_id": category_id
            }
        })

    return documents


def main():
    books = fetch_books()
    corpus = build_corpus(books)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(corpus, file, indent=2, ensure_ascii=False)

    print(f"Fetched books: {len(books)}")
    print(f"Corpus documents created: {len(corpus)}")
    print(f"Saved to: {OUTPUT_FILE}")

    for document in corpus:
        print(f"- {document['metadata']['title']}")


if __name__ == "__main__":
    main()