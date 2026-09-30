from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()


# Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)


# Prompt with conversation history
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a library assistant. "
        "Use only the information available in the conversation history. "
        "If the current question depends on information that is not in the "
        "conversation history, say that you do not have enough context. "
        "Do not use outside knowledge."
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])


# Basic LCEL chain
chain = prompt | model


# Session-scoped in-memory store
session_store = {}


def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()

    return session_store[session_id]


# Add automatic conversation memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)


print("=" * 65)
print("PART C - CONVERSATION MEMORY")
print("=" * 65)


# First conversation
print("\nSESSION: user-42")

response1 = chain_with_memory.invoke(
    {
        "question": "Dune by Frank Herbert is a science fiction novel. Tell me about this book."
    },
    config={
        "configurable": {
            "session_id": "user-42"
        }
    }
)

print("\nQuestion 1:")
print("Tell me about Dune by Frank Herbert.")

print("\nAnswer 1:")
print(response1.content)


# Follow-up question using the SAME session
response2 = chain_with_memory.invoke(
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

print("\nAnswer 2:")
print(response2.content)


# New session
print("\n" + "-" * 65)
print("SESSION: user-99 (NEW SESSION)")
print("-" * 65)

response3 = chain_with_memory.invoke(
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

print("\nAnswer from new session:")
print(response3.content)


print("\n" + "=" * 65)
print("Conversation memory test completed successfully.")
print("=" * 65)