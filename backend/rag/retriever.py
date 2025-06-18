from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
import glob
import json
import os

amount_similar_chunks = 4

# Context Data
data_path = "./data"
persist_dir = "./vector_store"
existing_file = "./embedded_files.json"

def load_embedded_files():
    if os.path.exists(existing_file):
        with open(existing_file, "r") as f:
            return set(json.load(f))
    return set()

def save_embedded_files(file_paths):
    with open(existing_file, "w") as f:
        json.dump(sorted(list(file_paths)), f, indent=2)

def get_retriever():

    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    docs = []

    current_files = set(glob.glob(f"{data_path}/**/*.pdf", recursive=True) + glob.glob(f"{data_path}/**/*.txt", recursive=True))
    embedded_files = load_embedded_files()
    new_files = current_files - embedded_files
    deleted_files = embedded_files - current_files

    if new_files or deleted_files:
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

        save_embedded_files(current_files)
        print("rebuilding...")

    else:
        vector_store = Chroma(persist_directory=persist_dir,
                              embedding_function=embeddings)

    return vector_store.as_retriever(search_kwargs={"k": amount_similar_chunks})