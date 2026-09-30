\# Week 6 Project — Library AI Assistant



\## Overview



The Library AI Assistant is a fully integrated AI-powered library application developed during Week 6.



The project combines:



\* LangChain RAG

\* RecursiveCharacterTextSplitter

\* MultiQueryRetriever

\* Structured output

\* Session-scoped memory

\* Availability tool calling

\* Resilient .NET AI service client

\* Retry and circuit-breaker handling

\* End-to-end streaming

\* Angular chat interface

\* FastAPI AI service



\## System Architecture



The complete data flow is:



Angular Chat UI

↓

.NET `/api/assistant/ask/stream`

↓

Resilient AI Service Client

↓

FastAPI `/ask/stream`

↓

LangChain RAG Chain

↓

Retriever + Availability Tool + Session Memory

↓

LLM

↓

Streaming response

↓

FastAPI → .NET → Angular



\## Main Components



\### 1. Angular Frontend



The Angular application provides a minimal chat interface where the user can:



\* Enter a library-related question

\* Send the question to the .NET API

\* Receive the AI response progressively

\* See an unavailable message when the AI service is down



The frontend uses the streaming endpoint:



`POST http://localhost:5032/api/assistant/ask/stream`



\### 2. .NET Library API



The .NET API acts as the secure integration layer between Angular and the FastAPI AI service.



Main endpoint:



`POST /api/assistant/ask/stream`



The AI service client uses:



\* HTTP client

\* Retry handling

\* Timeout handling

\* Circuit-breaker handling

\* Streaming response support



If the AI service cannot be reached, the API returns an unavailable response instead of allowing the application to crash.



\### 3. FastAPI AI Service



The FastAPI service provides the AI endpoints:



\* `GET /health`

\* `POST /ask`

\* `POST /ask/stream`



The streaming endpoint sends the response incrementally using Server-Sent Events.



\### 4. LangChain RAG



The AI service uses a LangChain-based retrieval pipeline.



The pipeline includes:



\* RecursiveCharacterTextSplitter

\* Vector embeddings

\* Chroma vector database

\* MultiQueryRetriever

\* RAG prompt

\* LLM response generation



This allows the assistant to retrieve relevant library information before generating an answer.



\### 5. Availability Tool



The AI assistant can use the library availability functionality through the .NET Library API.



The availability endpoint is:



`GET /api/books/{id}/availability`



The tool allows the AI system to check whether a specific library book is available.



\### 6. Session-Scoped Memory



The AI service maintains conversation memory using a session ID.



Example:



First message:



`Remember this: the library test user is Eman.`



Follow-up:



`What did I just ask you to remember?`



The assistant correctly recalled:



`You asked me to remember that the library test user is Eman.`



This demonstrates multi-turn session memory.



\### 7. Streaming



The AI response is streamed through the complete application:



Angular

→ .NET

→ FastAPI

→ LangChain/LLM

→ FastAPI

→ .NET

→ Angular



The Angular interface displays the answer progressively instead of waiting for the complete response.



\## Resilience Testing



The AI service was intentionally stopped while the Angular application remained running.



The .NET API detected the connection failure and performed retry attempts.



After the AI service remained unavailable, the Angular interface displayed:



`AI service is temporarily unavailable.`



This demonstrates graceful failure handling instead of application hanging or crashing.



\## Project Structure



```text

Week6\_Project\_Library\_AI\_Assistant/

│

├── LibraryAPI/

│   ├── Controllers/

│   ├── Services/

│   ├── Models/

│   └── ...

│

├── ai-service/

│   ├── main.py

│   ├── .env

│   └── ...

│

├── library-angular/

│   ├── src/

│   └── ...

│

└── README.md

```



\## Known Limitations



\### In-Memory Session Store



Conversation memory is currently stored in memory.



The memory is therefore temporary and is not intended to survive application restarts.



\### No Persistent Memory



There is currently no persistent conversation database.



A future version could store sessions and conversation history in a persistent database.



\### Local Development Services



The project currently uses local development URLs for the .NET API and FastAPI service.



\## Week 6 Requirements Completed



\* LangChain RAG chain

\* Advanced retrieval

\* Structured output

\* Session-scoped memory

\* Availability tool

\* Resilient AI service client

\* Retry handling

\* Circuit-breaker handling

\* Streaming AI responses

\* Angular streaming chat UI

\* AI service failure handling

\* Multi-turn memory verification

\* Interactive Git rebase practice



\## Future Work



Multi-step agent behavior and LangGraph-based workflows are planned for Week 7.



