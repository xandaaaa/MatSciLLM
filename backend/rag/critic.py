from typing import List, Dict, Any
import json
from langchain_ollama import OllamaLLM


class Critic:
    def __init__(self, model: str = "mistral", temperature: float = 0.3):
        self.llm = OllamaLLM(model=model, temperature=temperature)

    def build_prompt(self, query: str, docs: List[str], answer: str, iteration: int = 1) -> str:
        doc_text = "\n".join([f"Doc {i+1}: {doc}" for i, doc in enumerate(docs)])
        return f"""
You are a helpful and thoughtful critique assistant.

Evaluate the given answer to a user query based on the retrieved documents.

Step 1: Analyze whether the answer is supported by the documents. Provide reasoning.
Step 2: Analyze whether the answer is useful and relevant to the query. Provide reasoning.
Step 3: Give scores in JSON format:
  - isSup: 0 (not supported) to 1 (fully supported)
  - isUse: 0 (not useful) to 1 (fully useful)

Iteration: {iteration}

Query:
{query}

Retrieved Documents:
{doc_text}

Answer:
{answer}

Critique and score:
""".strip()

    def run(self, query: str, docs: List[str], answer: str, max_iterations: int = 2) -> Dict[str, Any]:
        result = None
        best = {"isSup": 0.0, "isUse": 0.0}
        for i in range(1, max_iterations + 1):
            prompt = self.build_prompt(query, docs, answer, iteration=i)
            output = self.llm.invoke(prompt)
            result = self._parse_output(output)

            if result.get("isSup", 0) > best["isSup"]:
                best.update(result)

            if result["isSup"] >= 0.9 and result["isUse"] >= 0.9:
                break

        return best

    def _parse_output(self, output: str) -> Dict[str, Any]:
        try:
            # Look for the JSON part of the output (assuming it's at the end)
            json_start = output.rfind("{")
            json_str = output[json_start:]
            scores = json.loads(json_str)
            return {
                "raw_output": output.strip(),
                "isSup": float(scores.get("isSup", 0)),
                "isUse": float(scores.get("isUse", 0)),
            }
        except Exception as e:
            return {
                "raw_output": output.strip(),
                "error": f"Failed to parse scores: {e}",
                "isSup": 0.0,
                "isUse": 0.0,
            }
