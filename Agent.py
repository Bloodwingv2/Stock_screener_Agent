from typing import Annotated, TypedDict
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages

from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from colorama import Fore
from langgraph.prebuilt import ToolNode
from tools import simple_screener

llm_ollama = init_chat_model(model="ollama:llama3.2:latest") # initialize local LLM

# Create state with reducer functions
class StockState(TypedDict):
    messages: Annotated[list,add_messages]
    
# Define the Chatbot invoker function
def chatbot(state:StockState) -> StockState:
    """Invoke The llm and return responses"""
    return {"messages": [llm_ollama_tools.invoke(state["messages"])]}

# Define Conditional Edge Function
def router(state:StockState) -> str:
    """Route the messages to the appropriate tool or LLM"""
    last_message = state["messages"][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "Continue"
    else:
        return "END"
        

# Create and list the tools
tools_new = [simple_screener]
# Create a ToolNode for LangGraph
tool_node = ToolNode(tools_new)
# Bind tools directly to the LLM (not the ToolNode)
llm_ollama_tools = llm_ollama.bind_tools(tools_new)


# Create the state graph
graph_builder = StateGraph(StockState)
graph_builder.add_node("Chatbot", chatbot)
graph_builder.add_node("Router", router)
graph_builder.add_node("ToolNode", tool_node)

graph_builder.add_edge(START, "Chatbot")
graph_builder.add_conditional_edges(
    "Chatbot",
    router,
    {
        "Continue": "ToolNode",
        "END": END,
    },
)
graph_builder.add_edge("ToolNode","Chatbot")

# Add Memory and Compile Graph
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# Build call loop and run it

if __name__ == "__main__":
    while True:
        user_input = input("Pass your prompt Here:")
        if "exit" in user_input.lower(): # exit clause for our agent
            print("\nExiting... Agent")
            break
        res = graph.invoke({"messages": [{"role": "user", "content": user_input}]}, config = {"configurable":{"thread_id":1234}})
        print(Fore.LIGHTYELLOW_EX + res["messages"][-1].content + Fore.RESET) # colour the Agent CMD