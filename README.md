# Stock Screener Agent

An AI-powered CLI based stock screener agent built with LangGraph, LangChain.

---
<img width="1576" height="607" alt="New ui 1" src="https://github.com/user-attachments/assets/08c74ade-bc3b-4985-9a61-dba0a8551c07" />

---
## Fetch Financial Data
Use Local AI models from Ollama to fetch Financial information from Yahoo finance for any stock related data
<br>
<img width="1570" height="857" alt="ui 2" src="https://github.com/user-attachments/assets/34c8198d-dc3d-46c7-98b3-4d7e4285d70a" />

---
## Pagination / Offset Values

Decide which page of data to fetch — the 1st, 2nd, or beyond. This lets you explore **more than just the first results page
<br>
<img width="1568" height="542" alt="ui 3" src="https://github.com/user-attachments/assets/596fc410-23aa-4ac2-a559-e97dd0a388f0" />
<img width="1598" height="659" alt="ui 4" src="https://github.com/user-attachments/assets/2fd0307b-c9a2-4b6c-837b-b1e416779d18" />

---
## Memory with LangGraph
Leverages **LangGraph’s built-in memory saver** to persist data between states. This gives the agent **contextual memory** for previously fetched data.
<br>
<img width="1555" height="459" alt="ui 5" src="https://github.com/user-attachments/assets/39d0a895-05ed-4223-8d37-eb0bae894432" />

---
## Quick Commands
- Check **today’s biggest gainers/losers** instantly  
- Discover **valuable small-cap opportunities**  
- Get a **stat sheet + analyst recommendation** (Buy / Sell)
- 
<img width="1576" height="473" alt="ui 6" src="https://github.com/user-attachments/assets/d2702c47-8d71-436c-b20d-5ccf464a59cb" />
Find valuable small cap opportunities and get a stat sheet and recommended analyst rating to determine whether we should buy or sell the stock

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



