print("Starting Personal AI Assistant...")

from typing import TypedDict
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END

print("Loading Llama model...")

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

class AssistantState(TypedDict):
    question: str
    answer: str

def assistant(state: AssistantState):
    print("Generating AI response...")
    response = llm.invoke(state["question"])
    return {"answer": response.content}

graph = StateGraph(AssistantState)

graph.add_node("assistant", assistant)
graph.add_edge(START, "assistant")
graph.add_edge("assistant", END)

app = graph.compile()

print("Running LangGraph...")

result = app.invoke({
    "question": "What is Artificial Intelligence?",
    "answer": ""
})

print("\nAI Assistant Response:")
print(result["answer"])

print("\nAssistant completed successfully!")

