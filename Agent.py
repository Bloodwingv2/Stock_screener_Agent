from typing import Annotated, TypedDict
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages

from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from colorama import Fore


llm_ollama = init_chat_model(model="ollama:llama3.2:latest") # initialize local LLM

# Create state with reducer functions

class StockState(TypedDict):
    messages: Annotated[list,add_messages]
    
# Define the Chatbot invoker function
def chatbot(state:StockState) -> StockState:
    """Invoke The llm and return responses"""
    return {"messages": [llm_ollama.invoke(state["messages"])]}

# Create the state graph
graph_builder = StateGraph(StockState)
graph_builder.add_node("Chatbot", chatbot)
graph_builder.add_edge(START, "Chatbot")
graph_builder.add_edge("Chatbot", END)

# Add Memory and Compile Graph
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# Build call loop and run it

if __name__ == "__main__":
    while True:
        user_input = input("Pass your prompt Here:")
        res = graph.invoke({"messages": [{"role": "user", "content": user_input}]}, config = {"configurable":{"thread_id":1234}})
        print(Fore.LIGHTYELLOW_EX + res["messages"][-1].content + Fore.RESET) # colour the Agent CMD