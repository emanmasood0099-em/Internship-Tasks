from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory


load_dotenv()


# --------------------------------------------------
# 1. Structured Output Model
# --------------------------------------------------

class BookAnswer(BaseModel):
    answer: str = Field(
        description="The answer to the user's question"
    )

    confidence: str = Field(
        description="Must be high, medium, or low"
    )

    sources: list[str] = Field(
        description="Book titles used to answer the question"
    )


# --------------------------------------------------
# 2. Gemini Model
# --------------------------------------------------

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)


# --------------------------------------------------
# 3. Prompt with Conversation History
# --------------------------------------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a library assistant. "
        "Use only information available in the conversation history. "
        "The conversation may contain structured JSON responses from previous turns. "
        "If the answer cannot be determined from the conversation history, "
        "say that there is not enough context. "
        "Do not use outside knowledge. "
        "Return the answer using the required structured format."
    ),

    MessagesPlaceholder(variable_name="history"),

    ("human", "{question}")
])


# --------------------------------------------------
# 4. Structured Output
# --------------------------------------------------

structured_model = model.with_structured_output(BookAnswer)


# --------------------------------------------------
# 5. Structured Chain
# --------------------------------------------------

structured_chain = prompt | structured_model


# --------------------------------------------------
# 6. Convert BookAnswer to JSON string
# --------------------------------------------------
# This allows RunnableWithMessageHistory to save
# the response safely in conversation history.

structured_for_memory = structured_chain | RunnableLambda(
    lambda result: result.model_dump_json()
)


# --------------------------------------------------
# 7. Session-Scoped Memory
# --------------------------------------------------

session_store = {}


def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()

    return session_store[session_id]


# --------------------------------------------------
# 8. Add Memory Around Structured Chain
# --------------------------------------------------

memory_chain = RunnableWithMessageHistory(
    structured_for_memory,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)


# --------------------------------------------------
# 9. Convert JSON string back to BookAnswer
# --------------------------------------------------

structured_memory_chain = memory_chain | RunnableLambda(
    lambda result: BookAnswer.model_validate_json(result)
)


# --------------------------------------------------
# 10. Test
# --------------------------------------------------

print("=" * 70)
print("PART C - STRUCTURED OUTPUT + CONVERSATION MEMORY")
print("=" * 70)


# --------------------------------------------------
# SESSION user-42
# --------------------------------------------------

print("\nSESSION: user-42")


result1 = structured_memory_chain.invoke(
    {
        "question": (
            "Dune by Frank Herbert is a science fiction novel. "
            "Tell me about this book."
        )
    },
    config={
        "configurable": {
            "session_id": "user-42"
        }
    }
)


print("\nQuestion 1:")
print(
    "Dune by Frank Herbert is a science fiction novel. "
    "Tell me about this book."
)


print("\nStructured Answer 1:")
print("Answer:", result1.answer)
print("Confidence:", result1.confidence)
print("Sources:", result1.sources)

print("\nResult type:", type(result1).__name__)


# --------------------------------------------------
# Follow-up using SAME session
# --------------------------------------------------

result2 = structured_memory_chain.invoke(
    {
        "question": "What genre is it?"
    },
    config={
        "configurable": {
            "session_id": "user-42"
        }
    }
)


print("\nQuestion 2 (follow-up):")
print("What genre is it?")


print("\nStructured Answer 2:")
print("Answer:", result2.answer)
print("Confidence:", result2.confidence)
print("Sources:", result2.sources)

print("\nResult type:", type(result2).__name__)


# --------------------------------------------------
# NEW SESSION
# --------------------------------------------------

print("\n" + "-" * 70)
print("SESSION: user-99 (NEW SESSION)")
print("-" * 70)


result3 = structured_memory_chain.invoke(
    {
        "question": "What genre is it?"
    },
    config={
        "configurable": {
            "session_id": "user-99"
        }
    }
)


print("\nQuestion:")
print("What genre is it?")


print("\nStructured Answer from New Session:")
print("Answer:", result3.answer)
print("Confidence:", result3.confidence)
print("Sources:", result3.sources)

print("\nResult type:", type(result3).__name__)


print("\n" + "=" * 70)
print("Structured output + memory test completed successfully.")
print("=" * 70)
