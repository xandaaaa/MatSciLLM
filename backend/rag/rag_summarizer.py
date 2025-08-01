from langchain_ollama import OllamaLLM
from .prompts import prompt
from .retriever import get_retriever
from langchain_core.runnables import Runnable
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Tab 2
def build_rag_summarizer(model_name="llama3"):

    retriever = get_retriever()
    llm = OllamaLLM(model=model_name)

    class RAGChainRunnable(Runnable):
        def invoke(self, input_dict):
            question = input_dict["question"]

            vector_store = retriever.vectorstore
            all_metadatas = vector_store.get(include=["metadatas"])["metadatas"]
            all_dois = set(meta.get("doi") for meta in all_metadatas if meta.get("doi"))
            logger.info(f"all DOIs: {all_dois}")

            amount_similar_chunks = 3

            def generate_all_answers():
                for doi in all_dois:
                    filtered_retriever = vector_store.as_retriever(
                        search_kwargs={
                            "k": amount_similar_chunks,
                            "filter": {"doi": doi}
                        }
                    )

                    docs = filtered_retriever.invoke(question)

                    context = "\n\n".join([
                        f"DOI: {doc.metadata.get('doi', 'Not found')}\n{doc.page_content}"
                        for doc in docs
                    ])

                    prompt_input = prompt.invoke({
                        "context": context,
                        "question": question
                    })

                    yield f"\n\n=== Answer for DOI: {doi} ===\n\n"

                    token_stream = llm.stream(prompt_input)
                    for token in token_stream:
                        token_str = token if isinstance(token, str) else token.get("content", "")
                        if token_str:
                            yield token_str

                    yield "\n\n"
            return {
                "question": question,
                "stream": generate_all_answers()
            }

    return RAGChainRunnable()