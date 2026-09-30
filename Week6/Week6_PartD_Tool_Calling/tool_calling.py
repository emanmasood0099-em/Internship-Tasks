import requests

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

API_BASE_URL = "http://localhost:5032"


@tool
def check_book_availability(book_id: int) -> str:
    """Check whether a specific book by its numeric ID is currently available to borrow."""

    response = requests.get(
        f"{API_BASE_URL}/api/books/{book_id}/availability",
        timeout=10
    )

    if response.status_code != 200:
        return "Could not check availability right now."

    data = response.json()

    if data["isAvailable"]:
        return "Available"

    return "Currently borrowed"


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0
)

model_with_tools = model.bind_tools(
    [check_book_availability],
    tool_choice="auto"
)


def get_text(content):
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        texts = []

        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block.get("text", ""))

        return " ".join(texts)

    return str(content)


def main():

    question = "Is book 8 available right now?"

    print()
    print("=" * 60)
    print("PART D - TOOL RESULT FED BACK TO MODEL")
    print("=" * 60)

    print()
    print("USER QUESTION:")
    print(question)

    messages = [
        HumanMessage(content=question)
    ]

    # Step 1: Model decides whether to call the tool
    first_response = model_with_tools.invoke(messages)

    print()
    print("MODEL TOOL DECISION:")

    if first_response.tool_calls:
        for call in first_response.tool_calls:
            print("Tool name:", call["name"])
            print("Arguments:", call["args"])

            # Step 2: Execute the requested tool
            result = check_book_availability.invoke(call["args"])

            print("Tool result:", result)

            # Step 3: Feed the model response and tool result back
            messages.append(first_response)

            messages.append(
                ToolMessage(
                    content=result,
                    tool_call_id=call["id"]
                )
            )

        # Step 4: Model produces natural-language answer
        final_response = model_with_tools.invoke(messages)

        print()
        print("FINAL NATURAL-LANGUAGE ANSWER:")
        print(get_text(final_response.content))

    else:
        print("No tool call was requested.")


if __name__ == "__main__":
    main()