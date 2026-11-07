from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

response = llm.invoke(
    "Hello, how can you help me?"
)

print(response.content)
