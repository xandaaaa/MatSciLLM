from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
import glob
import json

amount_similar_chunks = 4

# Context Data
data_path = "./data"
persist_dir = "./vector_store"

def get_retriever():

    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
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