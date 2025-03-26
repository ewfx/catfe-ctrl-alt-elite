import typer
import os
import subprocess
import sys
from dotenv import load_dotenv
from finsure.payment import main as payment_main
from finsure.compliance import main as compliance_main
from finsure.CICD import create_github_action
from finsure.regulatory_compliance import run_glue  # Import regulatory compliance function
import webbrowser

# Load environment variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", "..", ".env")
load_dotenv(ENV_PATH)
PROJECT_ROOT = "/Users/Jyothikamalesh/Projects/testing tool/finsure/src/finsure/payments-testing"

app = typer.Typer(add_completion=False)

# @app.command()
# def payment(file_path: str):
#     """payment: Process payments using the specified file."""
#     absolute_path = os.path.abspath(file_path)
#     payment_main(absolute_path)

# @app.command()
# def compliance(file_path: str):
#     """compliance: Run compliance checks on the specified file."""
#     absolute_path = os.path.abspath(file_path)
#     compliance_main(absolute_path)

@app.command("github-testflow")
def git_action_wf():
    """Generate GitHub Actions workflow,A Plug and Play CICD solution for github repo ."""
    create_github_action()

# @app.command("Contextaware-chatbot-defender")
# def chat_agent_test():
#     """Launch the chatbot automation testing app."""
#     command = [sys.executable, "-m", "streamlit", "run", os.path.join(BASE_DIR, "Chat_agent_test.py")]
#     subprocess.run(command, check=True)





import time  # Import time module

@app.command("paymentapi-defender")
def run_docker():
    """Transaction API test with Cause analysis,Explainablity and Remediation of test cases."""
    typer.echo("[INFO] Starting Docker containers using docker-compose...")
    try:
        subprocess.run(["docker-compose", "up", "--build", "-d"], cwd=PROJECT_ROOT, check=True)
    except subprocess.CalledProcessError:
        typer.echo("[ERROR] Failed to start Docker containers.")
        raise typer.Exit(1)

    typer.echo("[INFO] Opening frontend in browser at http://localhost:8501 ...")
    webbrowser.open("http://localhost:8501")

@app.command("codebase-defender")
def regulatory_compliance(file_path: str):
    """RAG powered regulatory compliance test function generator and execution pipeline."""
    absolute_path = os.path.abspath(file_path)
    run_glue(absolute_path)

@app.command("creditengine-defender")
def creditengine_defender():
    """Credit engine ML API test cases generation and execution."""
    generate_script = "/Users/Jyothikamalesh/Projects/testing tool/finsure/src/finsure/generation.py"
    
    if not os.path.exists(generate_script):
        typer.echo("[ERROR] generate.py not found.")
        raise typer.Exit(1)

    typer.echo("[INFO] Running Credit Engine test case generation and execution...")
    try:
        subprocess.run([sys.executable, generate_script], check=True)
        typer.echo("[SUCCESS] Credit Engine testing completed!")
    except subprocess.CalledProcessError:
        typer.echo("[ERROR] Failed to execute Credit Engine tests.")
        raise typer.Exit(1)


@app.command("prompt-defender")
def creditengine_defender():
    """ Prompt injection and Chatbot UI Automation test"""
    chatbot_script = os.path.join(BASE_DIR, "chatbot_testing.py")
    if not os.path.exists(chatbot_script):
        typer.echo("[ERROR] chatbot_testing.py not found.")
        raise typer.Exit(1)
    typer.echo("[INFO] Launching Chatbot Security Testing in Streamlit...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", chatbot_script], check=True)
        typer.echo("[SUCCESS] Chatbot Testing UI Launched!")
    except subprocess.CalledProcessError:
        typer.echo("[ERROR] Failed to launch Chatbot Testing UI.")
        raise typer.Exit(1)

@app.command("ui-defender")
def ui_testing():
    """ NLP instructed Agentic UI automation tool """
    script_path = os.path.join(BASE_DIR, "ui_testing.py")
    if not os.path.exists(script_path):
        typer.echo(f"Error: {script_path} not found.")
        raise typer.Exit(1)
    command = [sys.executable, "-m", "streamlit", "run", script_path]
    subprocess.run(command, check=True)

# @app.command("stop-docker")
# def stop_docker():
#     """ Stop and remove running Docker containers."""
#     typer.echo("[INFO] Stopping all Docker containers...")
#     try:
#         subprocess.run(["docker-compose", "down"], cwd=PROJECT_ROOT, check=True)
#         typer.echo("[SUCCESS] Containers stopped and removed.")
#     except subprocess.CalledProcessError:
#         typer.echo("[ERROR] Failed to stop Docker containers.")
#         raise typer.Exit(1)



if __name__ == "__main__":
    app()