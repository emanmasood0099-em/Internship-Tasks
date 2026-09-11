import os

from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

history = [
    {"role": "user", "parts": [{"text": "My name is Sam."}]}
]

response1 = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=history
)

print("User: My name is Sam.")
print("Assistant:", response1.text)

history.append({
    "role": "model",
    "parts": [{"text": response1.text}]
})

history.append({
    "role": "user",
    "parts": [{"text": "What's my name?"}]
})

response2 = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=history
)

print("User: What's my name?")
print("Assistant:", response2.text)

history.append({
    "role": "model",
    "parts": [{"text": response2.text}]
})

print()
print("Conversation history:")
for message in history:
    print(message["role"], ":", message["parts"][0]["text"])