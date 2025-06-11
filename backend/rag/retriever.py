from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import glob

amount_similar_chunks = 4
data_path = r"/Users/xanderyap/Documents/Cork/Work/LLM/MatSciLLM/backend/data"

def get_retriever(persist_dir="./vector_store"):
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    if os.path.exists(persist_dir):
        vector_store = Chroma(persist_directory=persist_dir,
                              embedding_function=embeddings)
        return vector_store.as_retriever(search_kwargs={"k": amount_similar_chunks})

    docs = []

    for file in glob.glob(f"{data_path}/**/*.pdf", recursive=True):
        docs.extend(PyPDFLoader(file).load())

    # Testing purposes
    for file in glob.glob(f"{data_path}/**/*.txt", recursive=True):
        docs.extend(TextLoader(file).load())
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    vector_store = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    return vector_store.as_retriever(search_kwargs={"k": amount_similar_chunks})