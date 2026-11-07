
import streamlit as st
import uuid
from datetime import datetime

from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from tools import calculate_sum


# -----------------------------------
# 1. Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="🤖",
    layout="centered"
)


# -----------------------------------
# 2. Create AI Agent
# -----------------------------------

@st.cache_resource
def build_agent():

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    memory = MemorySaver()

    agent = create_react_agent(
        model=llm,
        tools=[calculate_sum],
        checkpointer=memory
    )

    return agent


agent = build_agent()


# -----------------------------------
# 3. Initialize Session Memory
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())


# -----------------------------------
# 4. Application Title
# -----------------------------------

st.title("🤖 Personal AI Assistant")

st.caption(
    "Powered by Llama 3.2, LangChain and LangGraph"
)

st.write(
    "Hello! I am your personal AI assistant. "
    "Ask me anything!"
)


# -----------------------------------
# 5. Display Previous Chat Messages
# -----------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------------
# 6. Chat Input
# -----------------------------------

question = st.chat_input("Ask me anything...")


# -----------------------------------
# 7. Process User Question
# -----------------------------------

if question:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                # Check date-related questions
                date_keywords = [
                    "date",
                    "today",
                    "current date",
                    "today's date",
                    "what day",
                    "current year"
                ]

                if any(
                    word in question.lower()
                    for word in date_keywords
                ):

                    # Get actual computer date and time
                    current_date = datetime.now().astimezone()

                    answer = current_date.strftime(
                        "Today's date is %A, %d %B %Y."
                    )

                else:

                    # Send question to LangGraph agent
                    response = agent.invoke(
                        {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": question
                                }
                            ]
                        },
                        config={
                            "configurable": {
                                "thread_id":
                                st.session_state.thread_id
                            }
                        }
                    )

                    # Get assistant response
                    answer = response["messages"][-1].content

            except Exception as e:

                answer = f"An error occurred: {str(e)}"

        # Display assistant response
        st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# -----------------------------------
# 8. Clear Chat Button
# -----------------------------------

if st.button("🗑️ Clear Chat"):

    st.session_state.messages = []
    st.session_state.thread_id = str(uuid.uuid4())

    st.rerun()
