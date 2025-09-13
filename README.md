# Stock Screener Agent

## Pre-requisites 
An AI-powered CLI based stock screener agent built with LangGraph, LangChain, Llama3.2 for lightweight processing.  
👉 Requires [Ollama](https://ollama.ai/) installed and running locally.  

⚡ **After installation, Open CMD and run:**
```bash
ollama pull llama3.2:latest
```
## Product Overview
An AI-powered CLI based stock screener agent built with LangGraph, LangChain, Llama3.2 for lightweight processing.
<br><br>
<img width="1576" height="607" alt="New ui 1" src="https://github.com/user-attachments/assets/08c74ade-bc3b-4985-9a61-dba0a8551c07" /> 

https://github.com/user-attachments/assets/a67ba317-6cfd-4eed-b0bd-429fecadf534

---

## Agent State Flow Diagram (Langgraph Flow)
Following Flowchart describes the Agent Flow loop during execution

<img width="254" height="372" alt="Agent Graph" src="https://github.com/user-attachments/assets/f0d973d7-54ca-44dc-8231-55babdafdef6" />

---
## Memory with LangGraph
Leverages **LangGraph’s built-in memory saver** to persist data between states. This gives the agent **contextual memory** for previously fetched data.
<br><br>

https://github.com/user-attachments/assets/ddfe56e8-a3db-4f85-961d-107747ce3b03

---
## Fetch Financial Data
Use a lightweight llama3.2 model from Ollama to fetch Financial information from Yahoo finance for any stock related data
<br><br>

https://github.com/user-attachments/assets/8a054a23-1ac6-4edb-a8e0-46efe11da23f

---
## Pagination / Offset Values

Decide which page of data to fetch — the 1st, 2nd, or beyond. This lets you explore more than just the first results page
<br><br>
<img width="1576" height="473" alt="ui 6" src="https://github.com/user-attachments/assets/d2702c47-8d71-436c-b20d-5ccf464a59cb" />

---

## Quick Commands
- Check **today’s biggest gainers/losers** instantly  
- Discover **valuable small-cap opportunities**  
- Get a **stat sheet + analyst recommendation** (Buy / Sell)
<br><br>

---

## Installation

### Prerequisites
- Python 3.10 or higher
- Git

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Bloodwingv2/Stock_screener_Agent.git
   cd Stock_screener_Agent
   ```

2. **Install with uv (creates venv and installs dependencies automatically)**
   ```bash
   uv sync
   ```

3. **Activate the venv**
   ```bash
   .venv\Scripts\activate.bat
   ```
   
4. **Run the stock screener:**
   ```bash
   stockscreener
   ```

## Dependencies

This project uses the following lightweight dependencies:
- `colorama` - Terminal colors and processing animations
- `langchain` - AI framework for utilizing Annotations like AIMessage
- `langchain-ollama` - Ollama integration to use local llama3.2 model for lightweight blazingly fast inference
- `langgraph` - AI workflow management
- `rich` - Beautiful terminal output
- `yfinance` - To fetch valid Stock market data page wise (offset)

Total installation size: ~50-100MB

## Development

For development, follow the same installation steps above. Customize your code as per your free-will and finally write.
  ```bash
   pip install -e .
   ```
The above command will install the the entire codebase as a pip package in your venv as an editable format allowing any code changed to reflect immediately in the final package for your local machine

## Usage
After installation, simply type:
```bash
stockscreener
```

The agent will present a welcome message, guide you with quick commands through the stock screening process with a beautiful, animated, interactive CLI with a unique and color full spinner powered by Llama3.2 from Ollama.












