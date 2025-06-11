import requests
import json
from rag.rag_chain import build_rag_chain

def main():
    rag_chain = build_rag_chain()

    output = rag_chain.invoke({"question": "how old is xander"})

    previous_token = ""
    for token_chunk in output["stream"]:

        if token_chunk.startswith(" ") or token_chunk in ",.?!":
            print(token_chunk, end="", flush=True)
        else:
            if previous_token and not previous_token.endswith(" "):
                print(" ", end="", flush=True)
            print(token_chunk, end="", flush=True)
        previous_token = token_chunk

if __name__ == "__main__":
    main()