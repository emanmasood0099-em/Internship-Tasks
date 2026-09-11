
## How to Run the AI Service
1. Create and activate a Python virtual environment.
2. Install dependencies with: pip install -r requirements.txt
3. Set the GEMINI_API_KEY environment variable.
4. Start the service with: python -m uvicorn main:app --reload
5. Open http://127.0.0.1:8000/docs to test the /summarize endpoint.

The .NET Library API and the AI service run independently in Week 4.
