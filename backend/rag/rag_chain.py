from langchain_ollama import OllamaLLM
from .prompts import prompt
from .retriever import get_retriever
from .critic import Critic
from langchain_core.runnables import Runnable

def build_rag_chain(model_name="llama3"):
    retriever = get_retriever()
    llm = OllamaLLM(model=model_name)

    class RAGChainRunnable(Runnable):
        def invoke(self, input_dict):
            question = input_dict["question"]
            docs = retriever.invoke(question)

            context = "\n\n".join([doc.page_content for doc in docs])

            prompt_input = prompt.invoke({
                "context": context,
                "question": question
            })

            results = []
            best_output = None

            def generate_answer():
                nonlocal best_output

                try:
                    token_stream = llm.stream(prompt_input)
                    answer_tokens = []

                    for token in token_stream:
                        token_str = token.strip() if isinstance(token, str) else token.get("content", "").strip()
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
                best_output = answer

            return {
                "question": question,
                "used_documents": [doc.page_content for doc in docs],
                "iterations": results,
                "final_answer": best_output or (results[-1]["answer"] if results else ""),
                "stream": generate_answer()
            }

    return RAGChainRunnable()