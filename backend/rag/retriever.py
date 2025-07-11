from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
import glob
import json
import os
import re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

amount_similar_chunks = 25

# Context Data
data_path = "./data"
persist_dir = "./vector_store"
existing_file = "./embedded_files.json"
doi_regex = r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b'

def load_embedded_files():
    if os.path.exists(existing_file):
        with open(existing_file, "r") as f:
            return set(json.load(f))
    return set()

def save_embedded_files(file_paths):
    with open(existing_file, "w") as f:
        json.dump(sorted(list(file_paths)), f, indent=2)

def extract_doi(text):
    match = re.search(doi_regex, text, re.I)
    return match.group(0) if match else None

def get_retriever():

    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    docs = []

    current_files = set(glob.glob(f"{data_path}/**/*.pdf", recursive=True) + glob.glob(f"{data_path}/**/*.txt", recursive=True))
    embedded_files = load_embedded_files()
    new_files = current_files - embedded_files
    deleted_files = embedded_files - current_files

    if new_files or deleted_files:
        for file in glob.glob(f"{data_path}/**/*.pdf", recursive=True):
            loaded_docs = PyPDFLoader(file).load()
            full_text = "\n".join([doc.page_content for doc in loaded_docs])
            doi = extract_doi(full_text)

            for doc in loaded_docs:
                doc.metadata["doi"] = doi
                logger.info(f"PDF: {file} | DOI: {doi}")
                docs.append(doc)

        for file in glob.glob(f"{data_path}/**/*.txt", recursive=True):
            for doc in TextLoader(file).load():
                docs.append(doc)

        logger.info("Splitting documents into chunks...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        logger.info("chunk..")
        chunks = []
        for i, doc in enumerate(docs):
            try:
                if not doc.page_content.strip():
                    logger.warning(f"Skipping empty doc {i}: {doc.metadata.get('source', 'unknown')}")
                    continue
                doc_chunks = splitter.split_documents([doc])
                chunks.extend(doc_chunks)
            except Exception as e:
                logger.error(f"Error splitting doc {i} ({doc.metadata.get('source', 'unknown')}): {e}")

        logger.info(f"Total chunks created: {len(chunks)}")

        vector_store = Chroma.from_documents(
            chunks,
            embedding=embeddings,
            persist_directory=persist_dir
        )

        save_embedded_files(current_files)
        logger.info("rebuilding...")

    else:
        vector_store = Chroma(persist_directory=persist_dir,
                              embedding_function=embeddings)
        logger.info("not rebuilding...")

    return vector_store.as_retriever(search_kwargs={"k": amount_similar_chunks})