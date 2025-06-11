from langchain_core.prompts import ChatPromptTemplate

template = """
Based on this context, answer the following question:
{question}

Ignore previous requests. You are an expert in material sciences.

Task:
Using the context provided above, answer the user's question clearly and concisely and if asked summarize material properties in a clear table. Do not make up information.

Here are relevant context snippets:
{context}
"""

prompt = ChatPromptTemplate.from_template(template)