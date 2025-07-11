from langchain_core.prompts import ChatPromptTemplate

template = """
Based on this context, answer the following question:
{question}

Ignore previous requests. You are an expert in material sciences.

Task:
Using the context provided below, answer the user's question clearly and concisely. Summarize relevant information in a clear table like this:

| DOI                          | Notes on Relevance                           |
|-----------------------------|-----------------------------------------------|
| 10.xxxx/abc123              | Contains mechanical properties of material X  |
| 10.yyyy/def456              | Discusses thermal conductivity and structure  |

Please say something to every single DOI.

Do not make up any information — only use what is present in the context.

Here are relevant context snippets (each snippet may include a DOI):
{context}

"""

prompt = ChatPromptTemplate.from_template(template)