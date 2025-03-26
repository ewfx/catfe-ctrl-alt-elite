import os
import streamlit as st
from rich.console import Console

console = Console()

def main(file_path: str):
    """Launches a Streamlit UI and displays the file content in a text area"""
    absolute_path = os.path.abspath(file_path)

    # Validate if file exists
    if not os.path.isfile(absolute_path):
        console.print(f"[bold red]Error:[/] File '{absolute_path}' not found.", style="bold")
        return

    # Try reading the file as text
    try:
        with open(absolute_path, "r", encoding="utf-8") as file:
            content = file.read()
    except UnicodeDecodeError:
        console.print(f"[bold red]Error:[/] '{absolute_path}' is not a text-readable file.", style="bold")
        return
    except Exception as e:
        console.print(f"[bold red]Error:[/] Unable to read file. {e}", style="bold")
        return

    # Create a temporary Streamlit script
    streamlit_script = f"""
import streamlit as st

st.title("Compliance File Viewer")

st.write("### File: {os.path.basename(absolute_path)}")

file_content = \"\"\"{content}\"\"\"
st.text_area("File Contents", file_content, height=400)
"""

    # Save it to a temp file and run Streamlit
    temp_script_path = "/tmp/compliance_viewer.py"
    with open(temp_script_path, "w", encoding="utf-8") as temp_file:
        temp_file.write(streamlit_script)

    console.print("[bold green]Launching Streamlit UI...[/]")
    os.system(f"streamlit run {temp_script_path}")
