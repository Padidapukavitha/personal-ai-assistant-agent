from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from tools import get_current_date, calculate_sum

# Initialize model
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

# Register tools
tools = [get_current_date, calculate_sum]

# Add memory
memory = MemorySaver()

# Create agent
agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=memory
)

config = {
    "configurable": {
        "thread_id": "assistant_1"
    }
}

print("Personal AI Assistant is ready!")

while True:
    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    response = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config=config
    )

    print("\nAssistant:", response["messages"][-1].content)

