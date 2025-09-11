# Stock Screener Agent

An AI-powered stock screener agent built with LangGraph, LangChain.

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

2. **Install with uv (creates venv automatically)**
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

For development, follow the same installation steps above. The `-e` flag installs the package in "editable" mode, so your changes are reflected immediately without reinstalling.

## Usage

After installation, simply run:
```bash
stockscreener
```

The agent will guide you with quick commands through the stock screening process with a beautiful, animated, interactive CLI.

