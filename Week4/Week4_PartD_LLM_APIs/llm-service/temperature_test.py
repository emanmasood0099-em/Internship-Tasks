import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

prompt = "Write a short creative description of a peaceful garden."

response_temp_0 = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=0
    )
)

response_temp_1 = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=1
    )
)

print("Temperature = 0")
print(response_temp_0.text)

print()
print("Temperature = 1")
print(response_temp_1.text)

print()
print("Comparison:")
if response_temp_0.text.strip() == response_temp_1.text.strip():
    print("The outputs are the same.")
else:
    print("The outputs are different.")
