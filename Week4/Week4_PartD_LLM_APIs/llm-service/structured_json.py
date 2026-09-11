import os
import json
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

title = "The Future of Artificial Intelligence"
description = "A book about how artificial intelligence is changing technology and everyday life."

prompt = f"""
Return ONLY valid JSON, no other text, in this exact shape:
{{
  "genre": "string",
  "summary": "one paragraph string"
}}

Book title: {title}
Description: {description}
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=0,
        response_mime_type="application/json"
    )
)

try:
    data = json.loads(response.text)
    print("Genre:", data["genre"])
except (json.JSONDecodeError, KeyError):
    print("Failed to parse valid JSON response.")
