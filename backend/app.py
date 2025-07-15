from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from rag.rag_chain import build_rag_chain
from fastapi.middleware.cors import CORSMiddleware

# Run: uvicorn app:app --reload

app = FastAPI()
rag_chain = build_rag_chain()

@app.post("/ask")
async def ask(request: Request):
    body = await request.json()
    question = body.get("question", "")

    # Add whitespaces and output
    def token_stream():
        output = rag_chain.invoke({"question": question})
        for token in output["stream"]:
            token_str = token if isinstance(token, str) else token.get("content", "")
            if not token_str:
                continue
            yield token_str

    return StreamingResponse(token_stream(), media_type="text/plain")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)