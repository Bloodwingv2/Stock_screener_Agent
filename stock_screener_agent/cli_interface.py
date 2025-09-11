# cli_interface.py - Modern Premium CLI Interface (Claude-style, polished)

import time
import asyncio
import re
from datetime import datetime
from contextlib import asynccontextmanager

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.rule import Rule
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.box import ROUNDED

console = Console()

class StockScreenerCLI:
    def __init__(self, graph=None):
        self.graph = graph
        self.session_id = f"session_{int(time.time())}"
        self.start_time = datetime.now()
        self.query_count = 0
        self.query_history = []

        # Sleek color palette
        self.primary = "#00d4aa"   # Teal
        self.secondary = "#6366f1" # Indigo  
        self.accent = "#f59e0b"    # Amber
        self.success = "#10b981"   # Emerald
        self.warning = "#f97316"   # Orange
        self.error = "#ef4444"     # Red
        self.muted = "#6b7280"     # Gray

    # ---------------- HEADER ---------------- #
    def display_header(self):
        """Minimal Claude-style header"""
        title = Text("StockScreener", style=f"bold {self.primary}")
        title.append(" AI Agent", style=f"bold {self.secondary}")
        
        subtitle = Text("AI-Powered Market Analysis", style=f"dim {self.muted}")
        owner =  Text("Made by Mirang Bhandari", style=f"dim {self.muted}")

        console.print()
        console.print(Align.center(title))
        console.print(Align.center(subtitle))
        console.print(Align.center(owner))
        console.print(Rule(style=f"dim {self.muted}"))
        console.print()

    def display_session_info(self):
        info = f"[dim {self.muted}]Session {self.session_id[-6:]} • {self.query_count} queries • {datetime.now().strftime('%H:%M')}[/]"
        console.print(Align.center(info))
        console.print()

    # ---------------- SCREENS ---------------- #
    def display_welcome(self):
        console.clear()
        self.display_header()
        self.display_session_info()

        table = Table.grid(padding=1)
        table.add_column(style=f"bold {self.primary}", min_width=20)
        table.add_column(style=f"dim {self.muted}", min_width=30)

        quick_cmds = [
            ("Show today's biggest gainers with a Offset of 0", "Display Today's Gainers"),
            ("Find Today's losers with a offset of 0", "Display Today's losers"),  
            ("What are the most active stocks at NASDAQ with a offset of 0?", "Display the most Active stocks"),
            ("What Tech growth stocks are currently in trend?", "Display the Growing technology stocks"),
            ("Find Small Cap opportunities with a offset of 1", "Display Small Cap Opportunities on page 1 of web search"),
        ]

        for cmd, tag in quick_cmds:
            table.add_row(f"→ {cmd}", f"# {tag}")

        console.print(Panel(table,
            title=f"[bold {self.primary}]Example Commands[/]",
            border_style=f"dim {self.primary}",
            box=ROUNDED,
            padding=(1, 2)
        ))
        console.print(f"[dim {self.muted}]Type [bold]/help[/] for commands • [bold]/exit[/] to quit[/]\n")

    def display_help(self):
        console.print(f"[bold {self.primary}]StockScreener AI[/] [dim {self.muted}]• Help & Commands[/]")
        console.print(Rule(style=f"dim {self.muted}"))

        cmd_table = Table.grid(padding=(0,1))
        cmd_table.add_column(style=f"bold {self.accent}", min_width=10)
        cmd_table.add_column(style="white")

        commands = [
            ("/help", "Show this help"),
            ("/clear", "Clear screen"),
            ("/exit", "Exit StockScreener AI"),
        ]
        for cmd, desc in commands:
            cmd_table.add_row(cmd, desc)

        console.print(cmd_table)
        console.print()

    # ---------------- INPUT / OUTPUT ---------------- #
    def display_user_input(self, query: str):
        console.print(f"[bold white]You[/] [dim {self.muted}]asked[/]")
        console.print(Panel(query, border_style=f"dim {self.secondary}", box=ROUNDED, padding=(0,1)))

    def display_ai_response(self, content: str):
        """Colorize tickers, bid/ask prices, and keep formatting intact."""
        lines = content.splitlines()
        formatted = Text()

        for line in lines:
            clean = line.rstrip()
            if not clean:
                formatted.append("\n")
                continue

            # --- Color tickers inside (TICKER) ---
            line = re.sub(
                r"\(([^)]+)\)",
                lambda m: f"[bold {self.secondary}]({m.group(1)})[/]",
                clean
            )

            # --- Color bid prices ---
            line = re.sub(
                r"(\$[\d]+\.\d+\s*bid)",
                lambda m: f"[bold {self.success}]{m.group(1)}[/]",
                line,
                flags=re.IGNORECASE
            )

            # --- Color ask prices ---
            line = re.sub(
                r"(\$[\d]+\.\d+\s*ask)",
                lambda m: f"[bold {self.accent}]{m.group(1)}[/]",
                line,
                flags=re.IGNORECASE
            )

            formatted.append(Text.from_markup(line + "\n"))

        console.print(f"[bold {self.primary}]StockScreener AI[/]")
        console.print(Panel(formatted, border_style=f"dim {self.primary}", box=ROUNDED, padding=(1, 2)))

    # ---------------- STATUS ---------------- #
    @asynccontextmanager
    async def show_thinking(self):
        states = ["Analyzing market data", "Processing fundamentals", "Calculating metrics", "Generating insights", "Reviewing trends", "Compiling report", "Optimizing results", "Finalizing response"]
        stop = asyncio.Event()

        async def animate():
            with Progress(
                SpinnerColumn(spinner_name=f"dots3"),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("", total=None)
                i = 0
                while not stop.is_set():
                    progress.update(task, description=f"[bold {self.primary}]{states[i % len(states)]}[/]")
                    await asyncio.sleep(2)
                    i += 1

        task = asyncio.create_task(animate())
        try:
            yield
        finally:
            stop.set()
            await task

    # ---------------- PROMPT ---------------- #
    def get_prompt(self) -> str:
        return f"[bold {self.primary}]❯[/] "

    # ---------------- MAIN LOOP ---------------- #
    async def run(self):
        self.display_welcome()
        while True:
            try:
                user_input = Prompt.ask(self.get_prompt(), console=console).strip()
                if not user_input:
                    continue

                if user_input.lower() in ["/exit", "/quit"]:
                    console.print(f"\n[{self.muted}]Goodbye![/]")
                    break
                elif user_input.lower() in ["/help", "/h"]:
                    self.display_help(); continue
                elif user_input.lower() == "/clear":
                    self.display_welcome(); continue

                console.print()
                self.display_user_input(user_input)

                if self.graph:
                    async with self.show_thinking():
                        result = await asyncio.to_thread(
                            self.graph.invoke,
                            {"messages":[{"role":"user","content":user_input}]},
                            config={"configurable":{"thread_id":self.session_id}}
                        )
                    response = result["messages"][-1].content
                else:
                    async with self.show_thinking():
                        await asyncio.sleep(2)
                        response = self.mock_response(user_input)

                self.display_ai_response(response)
                self.query_count += 1
                self.query_history.append((datetime.now(), user_input))

            except KeyboardInterrupt:
                console.print(f"\n[{self.warning}]Interrupted. Use /exit to quit.[/]")
                continue
            except Exception as e:
                console.print(Panel(str(e), border_style=f"dim {self.error}", box=ROUNDED))
