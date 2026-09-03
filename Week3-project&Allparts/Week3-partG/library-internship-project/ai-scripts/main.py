import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

client = genai.Client(api_key=api_key)

title = input("Enter book title: ").strip()
description = input("Enter book description: ").strip()

if not title or not description:
    print("Book title and description are required.")
    raise SystemExit(1)

prompt = f"""
You are a helpful librarian.

Book title: {title}
Book description: {description}

Please provide:
1. A short one-paragraph summary.
2. One suitable genre.

Clearly label both answers.
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print("\nAI Response:\n")
print(response.text)