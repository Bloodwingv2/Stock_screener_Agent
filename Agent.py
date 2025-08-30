from typing import Annotated, TypedDict
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode
from tools import simple_screener

# Import Rich for Enhance Terminal UI
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
import time
import sys

# Initialize Rich console
console = Console()

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

# Initialize Rich Format panel code to augment CLI
def display_welcome():
    """Display a welcome message with styling"""
    welcome_text = """
    Stock Screening AI Agent
    Version 1.0.0, Made by Mirang Bhandari :)
    Type 'help' for commands | 'exit' to quit
    """
    console.print(Panel(welcome_text, style="bold blue", title="Welcome", subtitle="Ready to help in your Stock Options"))

def display_help():
    """Display available commands"""
    help_text = """
    Available Prompt Commands:
    - simple_screener: Screen stocks based on criteria (Add "Simple_screener" along with your prompt for a accurate response)
    - help: Show this help message
    - exit: Exit the agent
    - clear: Clear the output
    """
    console.print(Panel(help_text, style="yellow", title="Help"))

def process_response(response):
    """Process and display the agent's response with proper formatting"""
    console.print(Panel(response["messages"][-1].content, 
                       style="green", 
                       title="Agent Response",
                       border_style="bright_blue"))

if __name__ == "__main__":
    display_welcome()
    
    while True:
        try:
            # Custom prompt with styling
            user_input = Prompt.ask("\n[bold blue]Stock Screener Agent[/bold blue]")
            
            # Command handling
            if user_input.lower() == "exit":
                console.print("\n[yellow]Shutting down agent...[/yellow]")
                time.sleep(1)
                console.print("[red]Goodbye! 👋[/red]")
                break
                
            elif user_input.lower() == "help":
                display_help()
                continue
                
            elif user_input.lower() == "clear":
                console.clear()
                display_welcome()
                continue
            
            # Show thinking spinner while processing
            with console.status("[bold blue]Thinking...[/bold blue]", spinner="dots"):
                res = graph.invoke(
                    {"messages": [{"role": "user", "content": user_input}]},
                    config={"configurable": {"thread_id": 1234}}
                )
            
            # Display formatted response
            process_response(res)
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user. Type 'exit' to quit.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")