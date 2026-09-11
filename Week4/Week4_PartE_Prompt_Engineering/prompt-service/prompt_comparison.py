import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

title = "The Alchemist"
description = "A young shepherd travels in search of a treasure and discovers lessons about dreams, courage, and self-discovery."


# 1. ZERO-SHOT
zero_shot_prompt = f"""
Suggest a genre and write a one-paragraph summary for this book.

Title: {title}
Description: {description}
"""


# 2. FEW-SHOT
few_shot_prompt = f"""
Suggest a genre and write a one-paragraph summary for the book.

Examples:

Book: "Dune"
Description: A desert planet, political intrigue, and a young hero caught in a struggle for power.
Genre: Science Fiction
Summary: A young hero becomes involved in a political and dangerous struggle on a desert planet.

Book: "Pride and Prejudice"
Description: Manners, relationships, and marriage in 19th century England.
Genre: Romance
Summary: A young woman navigates relationships and social expectations while discovering love.

Now classify this book:

Title: {title}
Description: {description}

Return:
Genre: ...
Summary: ...
"""


# 3. SYSTEM-LEVEL ROLE PROMPT
role_prompt = f"""
Title: {title}
Description: {description}

Give the genre and a one-paragraph summary.
"""

response_zero = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=zero_shot_prompt,
    config=types.GenerateContentConfig(
        temperature=0
    )
)

response_few = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=few_shot_prompt,
    config=types.GenerateContentConfig(
        temperature=0
    )
)

response_role = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=role_prompt,
    config=types.GenerateContentConfig(
        temperature=0,
        system_instruction=(
            "You are a professional library cataloguer. "
            "Analyze the book title and description. "
            "Return exactly two fields: Genre and Summary. "
            "The Summary must be one paragraph."
        )
    )
)


print("=== ZERO-SHOT ===")
print(response_zero.text)

print()
print("=== FEW-SHOT ===")
print(response_few.text)

print()
print("=== SYSTEM-LEVEL ROLE ===")
print(response_role.text)

print()
print("=== COMPARISON ===")
print("Zero-shot: direct instructions with no examples.")
print("Few-shot: examples guide the model's pattern and format.")
print("System-level role: the model follows a library cataloguer role and a fixed output format.")
