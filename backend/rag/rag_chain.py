from langchain_ollama import OllamaLLM
from .prompts import prompt_ask
from .retriever import get_retriever
from langchain_core.runnables import Runnable

# Tab 1
def build_rag_chain(model_name="llama3"):

    # Retrieve vector store
    retriever = get_retriever()
    llm = OllamaLLM(model=model_name)

    class RAGChainRunnable(Runnable):
        def invoke(self, input_dict):
            question = input_dict["question"]
            docs = retriever.invoke(question)

            context = "\n\n".join([
                f"DOI: {doc.metadata.get('doi', 'Not found')}\n{doc.page_content}"
                for doc in docs
            ])

            prompt_input = prompt_ask.invoke({
                "context": context,
                "question": question
            })

            results = []

            def generate_answer():
                try:
                    token_stream = llm.stream(prompt_input)
                    answer_tokens = []

                    for token in token_stream:
                        token_str = token if isinstance(token, str) else token.get("content", "")
                        if not token_str:
                            continue

                        answer_tokens.append(token_str)
                        yield token_str

                    yield "\n\n"

                except Exception as stream_err:
                    print(f"Error during streaming: {stream_err}")
                    yield f"[Stream error: {stream_err}]\n\n"

                answer = "".join(answer_tokens).strip()
                results.append({"answer": answer})

            return {
                "question": question,
                "used_documents": [doc.page_content for doc in docs],
                "iterations": results,
                "stream": generate_answer()
            }

    return RAGChainRunnable()