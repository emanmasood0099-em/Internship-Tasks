import os
import json
import asyncio
import requests

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

load_dotenv()

app = FastAPI(
    title="Week 6 Library AI Assistant",
    version="1.0.0"
)

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

CORPUS_PATH = r"D:\Internship-Tasks\Week5\Week5_Project\data\books_corpus.json"

API_BASE_URL = os.getenv(
    "LIBRARY_API_URL",
    "http://localhost:5080"
)

# ---------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------

class AskRequest(BaseModel):
    question: str
    session_id: str = "default"


class BookAnswer(BaseModel):
    answer: str = Field(
        description="The answer to the user's question"
    )
    confidence: str = Field(
        description="Must be high, medium, or low"
    )
    sources: list[str] = Field(
        description="Book titles used for the answer"
    )


# ---------------------------------------------------------
# Load Week 5 corpus - READ ONLY
# ---------------------------------------------------------

def load_corpus():
    with open(CORPUS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


books = load_corpus()

raw_book_text = "\n\n".join(
    book["text"] for book in books
)

# ---------------------------------------------------------
# Recursive Character Text Splitter
# ---------------------------------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = splitter.split_text(raw_book_text)

# ---------------------------------------------------------
# Gemini Embeddings + Chroma
# ---------------------------------------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

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
    collection_name="week6_project_library_ai"
)

base_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

# ---------------------------------------------------------
# Gemini Chat Model
# ---------------------------------------------------------

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0
)

# ---------------------------------------------------------
# MultiQueryRetriever
# ---------------------------------------------------------

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=model
)

# ---------------------------------------------------------
# Availability Tool
# ---------------------------------------------------------

@tool
def check_book_availability(book_id: int) -> str:
    """Check whether a specific book by numeric ID is currently available."""

    try:
        response = requests.get(
            f"{API_BASE_URL}/api/books/{book_id}/availability",
            timeout=10
        )

        if response.status_code != 200:
            return "Could not check availability right now."

        data = response.json()

        if data.get("isAvailable"):
            return "Available"

        return "Currently borrowed"

    except requests.RequestException:
        return "Library availability service is temporarily unavailable."


model_with_tools = model.bind_tools(
    [check_book_availability],
    tool_choice="auto"
)

# ---------------------------------------------------------
# Session Memory
# ---------------------------------------------------------

session_store = {}


def get_session_history(session_id: str) -> ChatMessageHistory:

    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()

    return session_store[session_id]


# ---------------------------------------------------------
# Structured Output Model
# ---------------------------------------------------------

structured_model = model.with_structured_output(
    BookAnswer
)

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def format_docs(documents):
    return "\n\n".join(
        document.page_content
        for document in documents
    )


def get_text(content):

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        texts = []

        for block in content:

            if isinstance(block, dict):
                if block.get("type") == "text":
                    texts.append(
                        block.get("text", "")
                    )

        return " ".join(texts)

    return str(content)


def guard_question(inputs):

    question = inputs["question"].strip()

    if len(question) < 3:
        raise ValueError(
            "Question too short to answer meaningfully."
        )

    return inputs


# ---------------------------------------------------------
# RAG Prompt
# ---------------------------------------------------------

rag_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a Library Knowledge Assistant.

Answer using the provided library context and conversation history.

If the answer is not available in the provided information,
say exactly:

I don't have that information in the provided documents.

Do not invent information.

For availability questions involving a numeric book ID,
use the availability tool when appropriate.
"""
    ),
    MessagesPlaceholder(
        variable_name="history"
    ),
    (
        "human",
        """
Library Context:
{context}

Current Question:
{question}
"""
    )
])

# ---------------------------------------------------------
# RAG + Memory Chain
# ---------------------------------------------------------

def retrieve_for_chain(question):

    documents = multi_query_retriever.invoke(
        question
    )

    return format_docs(documents)


rag_chain = (
    RunnableLambda(guard_question)
    |
    {
        "context": (
            RunnableLambda(
                lambda x: x["question"]
            )
            |
            RunnableLambda(
                retrieve_for_chain
            )
        ),
        "question": RunnableLambda(
            lambda x: x["question"]
        ),
        "history": RunnableLambda(
            lambda x: []
        )
    }
    |
    rag_prompt
    |
    model
    |
    StrOutputParser()
)


# ---------------------------------------------------------
# API Routes
# ---------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "week6-library-ai-assistant"
    }


@app.post("/ask")
def ask(request: AskRequest):

    session_id = request.session_id

    history = get_session_history(
        session_id
    )

    question = request.question.strip()

    if len(question) < 3:
        return {
            "answer": "Question too short to answer meaningfully.",
            "session_id": session_id
        }

    # -----------------------------------------------------
    # Availability tool flow
    # -----------------------------------------------------

    messages = [
        HumanMessage(content=question)
    ]

    first_response = model_with_tools.invoke(
        messages
    )

    if first_response.tool_calls:

        messages.append(first_response)

        for call in first_response.tool_calls:

            if call["name"] == "check_book_availability":

                result = check_book_availability.invoke(
                    call["args"]
                )

                messages.append(
                    ToolMessage(
                        content=result,
                        tool_call_id=call["id"]
                    )
                )

        final_response = model_with_tools.invoke(
            messages
        )

        answer = get_text(
            final_response.content
        )

    else:

        # -------------------------------------------------
        # RAG + session memory
        # -------------------------------------------------

        documents = multi_query_retriever.invoke(
            question
        )

        context = format_docs(
            documents
        )

        prompt_messages = [
            (
                "system",
                """
You are a Library Knowledge Assistant.

Use only the library context and conversation history.

Do not invent information.
"""
            )
        ]

        for message in history.messages:

            if isinstance(message, HumanMessage):

                prompt_messages.append(
                    ("human", message.content)
                )

            elif isinstance(message, AIMessage):

                prompt_messages.append(
                    ("assistant", message.content)
                )

        prompt_messages.append(
            (
                "human",
                f"""
Library Context:
{context}

Question:
{question}
"""
            )
        )

        response = model.invoke(
            prompt_messages
        )

        answer = get_text(
            response.content
        )

    # Save conversation
    history.add_user_message(
        question
    )

    history.add_ai_message(
        answer
    )

    return {
        "answer": answer,
        "session_id": session_id
    }


@app.post("/ask/stream")
async def ask_stream(request: AskRequest):

    question = request.question.strip()
    session_id = request.session_id

    if len(question) < 3:

        async def short_question():

            yield (
                "data: Question too short to answer meaningfully."
                "\n\n"
            )

            yield "data: [DONE]\n\n"

        return StreamingResponse(
            short_question(),
            media_type="text/event-stream"
        )

    history = get_session_history(
        session_id
    )

    async def event_generator():

        try:

            # ---------------------------------------------
            # Retrieve documents
            # ---------------------------------------------

            documents = await asyncio.to_thread(
                multi_query_retriever.invoke,
                question
            )

            context = format_docs(
                documents
            )

            # ---------------------------------------------
            # Build conversation
            # ---------------------------------------------

            prompt_messages = [
                (
                    "system",
                    """
You are a Library Knowledge Assistant.

Answer using only the provided library context
and conversation history.

Do not invent information.
"""
                )
            ]

            for message in history.messages:

                if isinstance(message, HumanMessage):

                    prompt_messages.append(
                        ("human", message.content)
                    )

                elif isinstance(message, AIMessage):

                    prompt_messages.append(
                        ("assistant", message.content)
                    )

            prompt_messages.append(
                (
                    "human",
                    f"""
Library Context:
{context}

Question:
{question}
"""
                )
            )

            # ---------------------------------------------
            # Stream response
            # ---------------------------------------------

            answer_parts = []

            for chunk in model.stream(
                prompt_messages
            ):

                text = get_text(
                    chunk.content
                )

                if text:

                    answer_parts.append(text)

                    yield (
                        f"data: {text}\n\n"
                    )

                    await asyncio.sleep(0)

            final_answer = "".join(
                answer_parts
            )

            # Save memory after complete response
            history.add_user_message(
                question
            )

            history.add_ai_message(
                final_answer
            )

            yield "data: [DONE]\n\n"

        except asyncio.CancelledError:

            print(
                "Streaming client disconnected."
            )

            raise

        except Exception as error:

            print(
                f"Streaming error: {error}"
            )

            yield (
                "data: AI service is temporarily unavailable."
                "\n\n"
            )

            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )


# ---------------------------------------------------------
# Startup information
# ---------------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    print("=" * 65)
    print("WEEK 6 LIBRARY AI ASSISTANT")
    print("=" * 65)
    print(f"Corpus records: {len(books)}")
    print(f"Generated chunks: {len(chunks)}")
    print(f"Library API: {API_BASE_URL}")
    print("FastAPI: http://localhost:8000")
    print("Health: http://localhost:8000/health")
    print("Ask: POST /ask")
    print("Streaming: POST /ask/stream")
    print("=" * 65)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
