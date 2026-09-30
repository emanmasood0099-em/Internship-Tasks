# Week 6 Part C — Structured Output & Conversation Memory

## Overview

This part implements structured output and session-scoped conversation memory using LangChain.

## 1. Structured Output

A Pydantic `BookAnswer` model is used with LangChain's `with_structured_output()`.

The model returns three structured fields:

- `answer`
- `confidence`
- `sources`

This avoids manually asking the model to return JSON and then using `json.loads()` to parse the response.

The returned result is a typed `BookAnswer` object.

## 2. Session-Scoped Conversation Memory

`RunnableWithMessageHistory` is used to maintain conversation history for each session.

Each conversation is identified using a unique `session_id`.

For example:

- `user-42` has its own conversation history.
- `user-99` starts with a separate empty conversation.

This allows different users or sessions to have separate conversation contexts.

## 3. Memory Test

The same session was tested with two questions.

First:

"Dune by Frank Herbert is a science fiction novel. Tell me about this book."

Follow-up:

"What genre is it?"

The second question was answered using the context stored in the same session.

A new session (`user-99`) was then asked the same follow-up question. Since the new session had no previous context, the system correctly reported that there was not enough context.

## 4. Combining Structured Output and Memory

The implementation combines both concepts in the same chain.

The structured `BookAnswer` result is converted into a JSON string before it is stored in conversation history.

When a response is returned to the application, the JSON string is converted back into a validated `BookAnswer` object.

This allows structured output and conversation memory to work together safely.

## 5. In-Memory Limitation

The current implementation uses an in-memory Python dictionary:

`session_store`

This means conversation history exists only while the application process is running.

If the FastAPI application or Python process restarts, all stored sessions and their conversation history are lost.

This is acceptable for this internship implementation because persistent memory is not required for this week.

## 6. Production Consideration

A production system should use persistent storage for conversation history.

Possible options include:

- Redis
- A database table

Persistent storage would allow conversation history to survive application restarts and support a real multi-user service more reliably.

## 7. Files

This folder contains:

- `structured_output.py` — structured output implementation
- `conversation_memory.py` — session-scoped conversation memory test
- `structured_memory_chain.py` — combined structured output and memory implementation
- `.env` — API configuration
- `.gitignore` — prevents sensitive and temporary files from being committed

## Result

Part C successfully demonstrates:

1. Structured output using Pydantic.
2. Session-scoped conversation memory.
3. Different context for different session IDs.
4. Combined structured output and conversation memory.
5. The limitation of temporary in-memory session storage.
