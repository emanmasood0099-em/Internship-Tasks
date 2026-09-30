import time

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


app = FastAPI(
    title="Week 6 Part F Streaming AI Service",
    version="1.0.0"
)


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask/stream")
def ask_stream(request: AskRequest):

    def event_generator():

        words = (
            "Artificial intelligence is technology that allows computers "
            "to learn, understand information, and perform tasks "
            "that normally require human intelligence."
        ).split()

        for word in words:

            time.sleep(1)

            yield f"data: {word}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )