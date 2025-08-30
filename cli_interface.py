# cli_interface.py - Enhanced CLI formatting (separate from LangGraph logic)

import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.tree import Tree

console = Console()

class StockScreenerCLI:
    def __init__(self, graph):
        self.graph = graph
        self.session_id = f"session_{int(time.time())}"
        self.start_time = datetime.now()
        self.query_count = 0

    def display_banner(self):
        """Professional banner"""
        banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                  ⚡ STOCK SCREENER AI                         ║
    ║                     Powered by LangGraph                      ║
    ╚═══════════════════════════════════════════════════════════════╝
        """
        console.print(Align.center(Text(banner, style="bold cyan")))
        
        # Session info
        info_table = Table.grid(padding=1)
        info_table.add_column(style="dim", justify="center")
        info_table.add_row("Version 1.0.0 | Created by Mirang Bhandari")
        info_table.add_row(f"Session: {self.session_id}")
        info_table.add_row(f"Started: {datetime.now().strftime('%H:%M:%S')}")
        
        console.print(Align.center(info_table))
        console.print()

    def display_welcome(self):
        """Enhanced welcome screen"""
        self.display_banner()
        
        # Quick start commands
        commands = Table(title="🚀 Quick Start Commands", show_header=False, box=None)
        commands.add_column("Command", style="bold cyan", no_wrap=True)
        commands.add_column("Description", style="white")
        
        commands.add_row("🔥 show day gainers", "Today's top performing stocks")
        commands.add_row("💰 find undervalued stocks", "Value investment opportunities")
        commands.add_row("📈 tech growth stocks", "High-growth technology companies")
        commands.add_row("📋 help", "See all available options")
        
        console.print(Panel(commands, title="Try These", border_style="green"))

    def display_help(self):
        """Comprehensive help system"""
        # Available screeners
        screeners = Table(title="📊 Stock Screeners Available")
        screeners.add_column("Type", style="bold cyan")
        screeners.add_column("Description", style="white")
        screeners.add_column("Good For", style="green")
        
        screener_options = [
            ("Day Gainers", "Biggest price increases today", "Quick opportunities"),
            ("Day Losers", "Biggest declines today", "Potential bargains"),
            ("Most Active", "Highest trading volume", "Market buzz"),
            ("Tech Growth", "Technology growth stocks", "Growth investors"),
            ("Undervalued Large Caps", "Cheap large companies", "Value investors"),
            ("Small Cap Gainers", "Rising small companies", "High risk/reward")
        ]
        
        for screen_type, desc, use_case in screener_options:
            screeners.add_row(screen_type, desc, use_case)
        
        console.print(screeners)
        
        # Usage examples
        examples = Panel(
            "[bold cyan]Example Queries:[/bold cyan]\n\n"
            "💬 \"Show me today's biggest gainers\"\n"
            "💬 \"Find undervalued technology stocks\"\n"
            "💬 \"What are the most active stocks?\"\n"
            "💬 \"Any good small cap opportunities?\"\n\n"
            "[dim]💡 Use natural language - I understand context![/dim]",
            title="🗣️ How to Ask",
            border_style="blue"
        )
        console.print(examples)

    def format_response(self, response_content: str) -> Panel:
        """Enhanced response formatting with stock-specific styling"""
        # Color-code financial data
        lines = response_content.split('\n')
        formatted_text = Text()
        
        for line in lines:
            if '$' in line and '%' in line:  # Price/percentage line
                if '+' in line or 'gain' in line.lower():
                    formatted_text.append(line + '\n', style="bold green")
                elif '-' in line or 'loss' in line.lower():
                    formatted_text.append(line + '\n', style="bold red")
                else:
                    formatted_text.append(line + '\n', style="white")
            elif 'Buy' in line:
                formatted_text.append(line + '\n', style="bold green")
            elif 'Sell' in line:
                formatted_text.append(line + '\n', style="bold red")
            else:
                formatted_text.append(line + '\n', style="white")
        
        return Panel(
            formatted_text,
            title="🤖 StockScreener AI",
            title_align="left",
            border_style="green",
            padding=(1, 2)
        )

    def show_thinking(self, message="Analyzing markets"):
        """Professional thinking animation"""
        return console.status(f"[bold blue]{message}...[/bold blue]", spinner="dots")

    def show_stats(self):
        """Display session statistics"""
        duration = str(datetime.now() - self.start_time).split('.')[0]
        
        stats = Table(title="📊 Session Stats", show_header=False)
        stats.add_column("Metric", style="cyan", no_wrap=True)
        stats.add_column("Value", style="white")
        
        stats.add_row("Queries Made", str(self.query_count))
        stats.add_row("Session Duration", duration)
        stats.add_row("Session ID", self.session_id[-8:])  # Show last 8 chars
        
        console.print(Panel(stats, border_style="blue"))

    def handle_error(self, error: Exception):
        """Professional error display"""
        error_panel = Panel(
            f"❌ [bold red]Error:[/bold red] {str(error)}\n\n"
            "🔧 [dim]Try rephrasing your request or type 'help' for guidance.[/dim]",
            title="Something went wrong",
            border_style="red"
        )
        console.print(error_panel)

    def run(self):
        """Main CLI loop with enhanced UX"""
        self.display_welcome()
        
        while True:
            try:
                # Enhanced prompt with query counter
                prompt_text = f"[bold blue]💭 You[/bold blue] [dim]({self.query_count} queries)[/dim]"
                user_input = Prompt.ask(prompt_text, console=console)
                
                # Handle commands
                if user_input.lower() in ["exit", "quit"]:
                    if Confirm.ask("\n[yellow]Exit Stock Screener?[/yellow]"):
                        self.show_stats()
                        console.print("\n[green]Thanks for using Stock Screener AI! 👋[/green]")
                        break
                    continue
                    
                elif user_input.lower() == "help":
                    self.display_help()
                    continue
                    
                elif user_input.lower() == "clear":
                    console.clear()
                    self.display_welcome()
                    continue
                    
                elif user_input.lower() == "stats":
                    self.show_stats()
                    continue
                
                # Process with agent
                with self.show_thinking("Processing your request"):
                    res = self.graph.invoke(
                        {"messages": [{"role": "user", "content": user_input}]},
                        config={"configurable": {"thread_id": self.session_id}}
                    )
                
                # Display enhanced response
                formatted_response = self.format_response(res["messages"][-1].content)
                console.print(formatted_response)
                
                # Update counter
                self.query_count += 1
                
                # Quick actions hint
                console.print(f"\n[dim]💡 Type 'help' for more options | 'stats' for session info | 'exit' to quit[/dim]")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]⚠️ Interrupted. Type 'exit' to quit gracefully.[/yellow]")
                continue
                
            except Exception as e:
                self.handle_error(e)