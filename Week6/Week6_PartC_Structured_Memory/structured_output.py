import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class BookAnswer(BaseModel):
    answer: str = Field(
        description="The answer to the user's question"
    )
    confidence: str = Field(
        description="Must be high, medium, or low"
    )
    sources: list[str] = Field(
        description="Book titles the answer was drawn from"
    )


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0
)

structured_model = model.with_structured_output(BookAnswer)

question = (
    "Which books are science fiction? "
    "Use the following library information: "
    "Dune by Frank Herbert is a science fiction novel. "
    "The Hobbit by J.R.R. Tolkien is a fantasy novel."
)

result = structured_model.invoke(question)

print("=" * 60)
print("PART C - STRUCTURED OUTPUT")
print("=" * 60)

print("\nQUESTION:")
print("Which books are science fiction?")

print("\nSTRUCTURED RESULT:")
print("Answer:", result.answer)
print("Confidence:", result.confidence)
print("Sources:", result.sources)

print("\nResult type:", type(result).__name__)

print("\nStructured output completed successfully.")