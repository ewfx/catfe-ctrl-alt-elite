import os
from rich.console import Console
from rich.text import Text

console = Console()

def main(file_path: str):
    """Reads and prints the contents of any text-readable file"""
    absolute_path = os.path.abspath(file_path)

    # Validate if file exists
    if not os.path.isfile(absolute_path):
        console.print(f"[bold red]Error:[/] File '{absolute_path}' not found.", style="bold")
        return

    # Try reading the file as text
    try:
        with open(absolute_path, "r", encoding="utf-8") as file:
            content = file.read()
            console.print(Text(content, style="bold cyan"))
    except UnicodeDecodeError:
        console.print(f"[bold red]Error:[/] '{absolute_path}' is not a text-readable file.", style="bold")
    except Exception as e:
        console.print(f"[bold red]Error:[/] Unable to read file. {e}", style="bold")
