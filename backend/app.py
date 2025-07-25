from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from rag.rag_chain import build_rag_chain
from rag.rag_summarizer import build_rag_summarizer
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import shutil
import os

# Run: uvicorn app:app --reload

app = FastAPI()
rag_chain_ask = build_rag_chain()
rag_summarizer = build_rag_summarizer()

# Get all pdfs that currently exist in the folder
@app.get("/getpdfs")
def list_pdfs():
    folder_path = "data"
    try:
        pdfs = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
        return JSONResponse(content=pdfs)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Upload PDF to data path
@app.post("/upload")
async def upload_pdfs(pdfs: List[UploadFile] = File(...)):
    for pdf in pdfs:
        dest = os.path.join("data", pdf.filename)
        with open(dest, "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)
    return {"message": "Uploaded", "files": [pdf.filename for pdf in pdfs]}

# First Tab (Ask Question)
@app.post("/ask")
async def ask(request: Request):
    body = await request.json()
    question = body.get("question", "")

    # Add whitespaces and output
    def token_stream():
        output = rag_chain_ask.invoke({"question": question})
        for token in output["stream"]:
            token_str = token if isinstance(token, str) else token.get("content", "")
            if not token_str:
                continue
            yield token_str

    return StreamingResponse(token_stream(), media_type="text/plain")

# Second Tab (Summarize every PDF)
@app.post("/summarizer")
async def summarize_text(request: Request):
    body = await request.json()
    question = body.get("question", "")

    # Add whitespaces and output
    def token_stream():
        output = rag_summarizer.invoke({"question": question})
        for token in output["stream"]:
            token_str = token if isinstance(token, str) else token.get("content", "")
            if not token_str:
                continue
            yield token_str

    return StreamingResponse(token_stream(), media_type="text/plain")

# TODO THIRD TAB

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)