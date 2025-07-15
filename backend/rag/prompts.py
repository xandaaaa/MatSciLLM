from langchain_core.prompts import ChatPromptTemplate

template = """
Based on this context, answer the following question:
{question}

Ignore previous requests. You are an expert in material sciences.

Task:
Using the context provided below, answer the user's question clearly and concisely. Summarize relevant information especially numerical data if found.

Do not make up any information — only use what is present in the context.

Here are relevant context snippets (each snippet may include a DOI):
{context}

"""

prompt = ChatPromptTemplate.from_template(template)