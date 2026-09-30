# Week 6 Part A - LangChain and LCEL

## Objective

Rebuild the Week 5 RAG pipeline using LangChain LCEL and add a custom input guard using RunnableLambda.

## LCEL Chain

Input Dictionary
    |
    v
RunnableLambda(guard_short_questions)
    |
    v
Runnable Mapping
    |
    +-- context -> Question -> Embedding -> Chroma Retrieval -> Document Formatting
    |
    +-- question -> Question
    |
    v
ChatPromptTemplate
    |
    v
ChatGoogleGenerativeAI
    |
    v
StrOutputParser
    |
    v
Final String Answer


## Data Type Trace

1. Initial Input

Type: dict

Example:

{
    "question": "What is the title of the book in the library?"
}


2. Input Guard

RunnableLambda(guard_short_questions) receives a dict.

Input type: dict
Output type: dict

If the question has fewer than 3 characters:

ValueError: Question too short to answer meaningfully.


3. Retrieval

The question is extracted from the input.

Type: str

The question is converted into a Gemini embedding.

Embedding type: list[float]

Chroma returns retrieved documents.

Retrieved documents type: list[str]


4. Document Formatting

Input type: list[str]
Output type: str


5. Runnable Mapping

The mapping produces a dictionary containing:

{
    "context": "...",
    "question": "..."
}

Type: dict


6. Chat Prompt

ChatPromptTemplate converts the dictionary into a chat prompt.

Output type: ChatPromptValue


7. Gemini Chat Model

ChatGoogleGenerativeAI processes the prompt.

Output type: AIMessage


8. Output Parser

StrOutputParser converts the AI message into plain text.

Output type: str


## Successful Test

Question:

What is the title of the book in the library?

Output:

The Alchemists Updated


## Short Question Guard Test

Test question:

A

Result:

ValueError: Question too short to answer meaningfully.


The stack trace identified:

app.py, line 85, guard_short_questions


This confirms that the guard executes before retrieval and before the Gemini model.


## LCEL Concepts Used

- RunnableLambda
- RunnablePassthrough
- Runnable mapping
- Pipe operator |
- ChatPromptTemplate
- ChatGoogleGenerativeAI
- StrOutputParser


## Git Checkpoint

feat: rebuild RAG chain using LangChain LCEL with custom input guard