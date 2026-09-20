\# Library Knowledge Assistant



\## Overview



The Library Knowledge Assistant is a manual RAG-based AI service that retrieves real book data from the existing .NET Library API and uses Chroma vector search with Gemini embeddings to answer questions.



\## Project Flow



SQL Server

↓

.NET Library API - GET /api/books

↓

Python Corpus Fetch Script

↓

books\_corpus.json

↓

Text Chunking

↓

Gemini Embeddings

↓

Chroma Vector Database

↓

FastAPI /ask Endpoint

↓

Retrieve Relevant Context

↓

Gemini LLM

↓

Answer + Source Attribution



\## Components



\### 1. .NET Library API



The existing Library API provides public book data through:



GET /api/books



The API is connected to the library database in SQL Server.



\### 2. Corpus Fetching



`fetch\_corpus.py` calls the public `/api/books` endpoint and converts the returned book data into short text documents.



The corpus is saved as:



`data/books\_corpus.json`



\### 3. Embeddings and Vector Database



`rag\_pipeline.py`:



\- Loads the book corpus.

\- Splits documents into chunks.

\- Generates embeddings using `gemini-embedding-001`.

\- Stores embeddings and metadata in Chroma.

\- Retrieves relevant documents for a question.



\### 4. FastAPI AI Service



`main.py` provides:



GET `/health`



POST `/ask`



The `/ask` endpoint:



1\. Receives the user's question.

2\. Generates a query embedding.

3\. Retrieves relevant documents from Chroma.

4\. Builds a grounded prompt.

5\. Sends the context to Gemini.

6\. Returns the answer and source book titles.



\### 5. Grounding



The assistant is instructed to answer only from the provided library context.



If the requested information is not available, it returns:



`I don't have that information in the provided documents.`



\### 6. Source Attribution



Answers include the title of the relevant source book.



\## Current Catalog Test



The current library catalog contains:



\- The Alchemists Updated



Verified questions include:



\- What is the title of the book in the library?

\- What is the author ID of the book in the library?

\- What is the category ID of the book in the library?



An unavailable question was also tested:



\- What is the price of The Alchemists Updated?



The unavailable information correctly returned the grounding fallback response.



\## Running the Project



\### Start the Library API



Run the existing .NET Library API so that:



`http://localhost:5032/api/books`



is available.



\### Fetch the Corpus



```powershell

python fetch\_corpus.py

