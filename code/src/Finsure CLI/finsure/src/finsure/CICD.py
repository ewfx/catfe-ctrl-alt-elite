import os
from rich.console import Console

console = Console()

github_action_yaml = """name: Run Tests on Pull Request

on:
  pull_request:
    branches:
      - main  # Modify this based on your branch structure

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set Up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Run Tests
        run: python your_test_script.py  # Replace with your test script
"""

def create_github_action():
    """Creates a GitHub Actions workflow file for testing"""
    workflow_dir = ".github/workflows"
    os.makedirs(workflow_dir, exist_ok=True)
    
    action_path = os.path.join(workflow_dir, "action.yml")
    with open(action_path, "w", encoding="utf-8") as f:
        f.write(github_action_yaml)
    
    console.print(f"[bold green]✅ GitHub Action workflow created at {action_path}[/]")

if __name__ == "__main__":
    create_github_action()
