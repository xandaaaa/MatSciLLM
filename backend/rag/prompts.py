from langchain_core.prompts import ChatPromptTemplate


template_ask = """
You are a materials science expert. Your job is to answer user questions strictly based on the provided context.

Task:
- Use only the information given in the context below. Do not speculate or generate information beyond it.
- Prioritize clarity and conciseness.
- Highlight any important numerical or material-specific data.

Question:
{question}

Context snippets (each may include a DOI):
{context}
"""

prompt_ask = ChatPromptTemplate.from_template(template_ask)


template_sum = """
Based on this context, answer the following question:
{question}

Ignore previous requests. You are an expert in material sciences.

Task:
Using the context provided below, answer the user's question clearly and concisely. Summarize relevant information especially numerical data if found.

Do not make up any information — only use what is present in the context.

If no related information is found simply output "No Information found".

Here are relevant context snippets (each snippet may include a DOI):
{context}

"""

prompt_sum = ChatPromptTemplate.from_template(template_sum)