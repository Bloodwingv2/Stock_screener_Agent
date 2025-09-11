# cli_interface.py - Modern Premium CLI Interface (Gemini-style, polished)

import time
import asyncio
import re
import os
import ctypes
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
from rich.style import Style


# ---------------- ENABLE ANSI ON WINDOWS ---------------- #
def enable_windows_ansi():
    """Enable ANSI escape codes in Windows CMD"""
    if os.name == "nt":
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)  # ENABLE_VIRTUAL_TERMINAL_PROCESSING

enable_windows_ansi()

# Rich auto-selects: "standard" (16), "256", or "truecolor"
console = Console(color_system="auto")


class StockScreenerCLI:
    def __init__(self, graph=None):
        self.graph = graph
        self.session_id = f"session_{int(time.time())}"
        self.start_time = datetime.now()
        self.query_count = 0
        self.query_history = []

        # Detect if running inside classic CMD (no WT_SESSION)
        is_cmd = os.name == "nt" and not os.environ.get("WT_SESSION")

        if is_cmd:
            # CMD-safe vivid ANSI palette
            self.primary   = "bright_cyan"
            self.secondary = "bright_blue"
            self.accent    = "bright_yellow"
            self.success   = "bright_green"
            self.warning   = "bright_magenta"
            self.error     = "bright_red"
            self.muted     = "bright_black"
        else:
            # Premium truecolor palette
            self.primary   = "#00f5d4"   # brighter teal
            self.secondary = "#3b82f6"   # vivid indigo
            self.accent    = "#facc15"   # golden yellow
            self.success   = "#22c55e"   # rich emerald
            self.warning   = "#e879f9"   # pink-magenta pop
            self.error     = "#f43f5e"   # vivid red
            self.muted     = "#9ca3af"   # soft gray

    # ---------------- HEADER ---------------- #
    def display_header(self):
        """Gemini-style ASCII header with gradient + subtitle"""
        logo_lines = [
            "  _________ __                 __       _________                                                ",
            " /   _____//  |_  ____   ____ |  | __  /   _____/ ___________   ____   ____   ____   ___________ ",
            " \\_____  \\\\   __\\/  _ \\_/ ___\\|  |/ /  \\_____  \\_/ ___\\_  __ \\_/ __ \\_/ __ \\ /    \\_/ __ \\_  __ \\",
            " /        \\|  | (  <_> )  \\___|    <   /        \\  \\___|  | \\/\\  ___/\\  ___/|   |  \\  ___/|  | \\/",
            "/_______  /|__|  \\____/ \\___  >__|_ \\ /_______  /\\___  >__|    \\___  >\\___  >___|  /\\___  >__|   ",
            "        \\/                  \\/     \\/         \\/     \\/            \\/     \\/     \\/     \\/        ",
        ]

        gradient_styles = [self.primary, self.secondary]
        for i, line in enumerate(logo_lines):
            style = Style(color=gradient_styles[i % len(gradient_styles)], bold=True)
            console.print(Align.center(Text(line, style=style)))

        subtitle = Text("AI-Powered Market Analysis", style=f"dim {self.muted}")
        console.print(Align.center(subtitle))
        console.print(Rule(style=f"dim {self.muted}"))

    def display_session_info(self):
        """Gemini-style bottom bar"""
        status = (
            f"[{self.muted}] session:{self.session_id[-4:]} "
            f"| queries:{self.query_count} "
            f"| {datetime.now().strftime('%H:%M')} [/] "
        )
        console.print(Align.center(status))
        console.print()

    # ---------------- SCREENS ---------------- #
    def display_welcome(self):
        console.clear()
        self.display_header()

        table = Table.grid(padding=1)
        table.add_column(style=f"bold {self.primary}", min_width=45)
        table.add_column(style=f"dim {self.muted}", min_width=30)

        quick_cmds = [
            ("Show today's biggest gainers with a Offset of 0", "Display Today's Gainers"),
            ("Find Today's losers with a offset of 0", "Display Today's losers"),
            ("What are the most active stocks at NASDAQ with a offset of 0?", "Display the most Active stocks"),
            ("What Tech growth stocks are currently in trend?", "Display the Growing technology stocks"),
            ("Find Small Cap opportunities with a offset of 1", "Display Small Cap Opportunities on page 1"),
        ]
        for cmd, tag in quick_cmds:
            table.add_row(f"→ {cmd}", f"# {tag}")

        console.print(Panel(table,
            title=f"[bold {self.secondary}]Example Commands[/]",
            border_style=f"{self.secondary}",
            box=ROUNDED,
            padding=(1, 2)
        ))

        console.print(f"[dim {self.muted}]Type [bold]/help[/] for commands • [bold]/exit[/] to quit[/]\n")
        self.display_session_info()

    def display_help(self):
        console.print(f"[bold {self.primary}]StockScreener AI[/] [dim {self.muted}]• Help & Commands[/]")
        console.print(Rule(style=f"dim {self.muted}"))

        cmd_table = Table.grid(padding=(0, 1))
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
        console.print(Panel(query, border_style=f"dim {self.secondary}", box=ROUNDED, padding=(0, 1)))

    def display_ai_response(self, content: str):
        """Lightweight Gemini-style response formatting"""
        lines = content.splitlines()
        formatted = Text()

        for line in lines:
            clean = line.rstrip()
            if not clean:
                formatted.append("\n")
                continue

            # Color tickers
            line = re.sub(
                r"\(([^)]+)\)",
                lambda m: f"[bold underline {self.secondary}]({m.group(1)})[/]",
                clean
            )

            # Bid prices
            line = re.sub(
                r"(\$[\d]+\.\d+\s*bid)",
                lambda m: f"[bold {self.success}]{m.group(1)}[/]",
                line,
                flags=re.IGNORECASE
            )

            # Ask prices
            line = re.sub(
                r"(\$[\d]+\.\d+\s*ask)",
                lambda m: f"[bold {self.accent}]{m.group(1)}[/]",
                line,
                flags=re.IGNORECASE
            )

            formatted.append(Text.from_markup(line + "\n"))

        console.print(f"[bold {self.primary}]StockScreener AI[/]")
        console.print(formatted)

    # ---------------- STATUS ---------------- #
    @asynccontextmanager
    async def show_thinking(self):
        """
        Async context manager to show a thinking spinner with changing text states.    
        """
        states = [
            "Analyzing market data", "Processing fundamentals", "Calculating metrics",
            "Generating insights", "Reviewing trends", "Compiling report",
            "Optimizing results", "Finalizing response"
        ]
        stop = asyncio.Event()

        async def animate():
            # Spinner and the text column are both styled bright magenta.
            # We pass plain strings into description to avoid markup parsing issues.
            with Progress(
                SpinnerColumn(spinner_name="dots3", style="bright_magenta"),
                TextColumn("[progress.description]{task.description}", style="bright_magenta"),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("", total=None)
                i = 0
                while not stop.is_set():
                    # Use plain text description (no markup)
                    progress.update(task, description=states[i % len(states)])
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
                    self.display_help()
                    continue
                elif user_input.lower() == "/clear":
                    self.display_welcome()
                    continue

                console.print()
                self.display_user_input(user_input)

                if self.graph:
                    async with self.show_thinking():
                        result = await asyncio.to_thread(
                            self.graph.invoke,
                            {"messages": [{"role": "user", "content": user_input}]},
                            config={"configurable": {"thread_id": self.session_id}}
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
