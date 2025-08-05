from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from rag.rag_chain import build_rag_chain
from rag.rag_summarizer import build_rag_summarizer
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import shutil
import os
import glob

# Run: uvicorn app:app --reload

app = FastAPI()
rag_chain_ask = None
rag_summarizer = None

# Get all pdfs that currently exist in the folder
@app.get("/getpdfs")
def list_pdfs():
    folder_path = "data"
    try:
        pdfs = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
        return JSONResponse(content=pdfs)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Delete all PDFs
@app.post("/clearpdfs")
def clear_pdfs():
    folder_path = "data"

    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    deleted_files = []

    for file_path in pdf_files:
        try:
            os.remove(file_path)
            deleted_files.append(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

    # Refresh backend (Provisionally)
    path_to_touch = "app.py" 
    os.utime(path_to_touch, None)

    return {"deleted": deleted_files}

# Upload PDF to data path
@app.post("/upload")
async def upload_pdfs(pdfs: List[UploadFile] = File(...)):
    for pdf in pdfs:
        dest = os.path.join("data", pdf.filename)
        with open(dest, "wb") as buffer:
            shutil.copyfileobj(pdf.file, buffer)

    # Refresh backend (Provisionally)
    path_to_touch = "app.py" 
    os.utime(path_to_touch, None)

    return {"message": "Uploaded", "files": [pdf.filename for pdf in pdfs]}

# First Tab (Ask Question)
@app.post("/ask")
async def ask(request: Request):

    global rag_chain_ask
    if rag_chain_ask is None:
        rag_chain_ask = build_rag_chain()

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

    global rag_summarizer
    if rag_summarizer is None:
        rag_summarizer = build_rag_summarizer()

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