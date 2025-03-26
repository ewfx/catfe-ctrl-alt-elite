import requests
import os
import subprocess
import argparse
from google import genai 
from google.genai import types
import re
import webbrowser
from multiprocessing import Process
from dotenv import load_dotenv
import sys

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key = GEMINI_API_KEY)



def fetch_news():
    """
    Queries the mock News API for articles related to 'CFPB' and returns a list of article bodies.
    """
    url = "http://127.0.0.1:8000/news/v2/everything"
    params = {"q": "CFPB"}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        # Extract the content of each article
        articles = data.get("articles", [])
        article_bodies = [article.get("content", "") for article in articles]
        
        print(f"[INFO] Retrieved {len(articles)} relevant articles.")
        return article_bodies
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error fetching news: {e}")
        return []



def do_inference(prompt):
    """
    Sends a prompt to the Gemini API and retrieves the generated code with temperature set to 0.
    """
    response = client.models.generate_content(
        model = "gemini-2.0-flash",
        contents = prompt,  # Set temperature to 0 for deterministic output
        config=types.GenerateContentConfig(
        temperature = 0,
        top_p = 0.99,
        top_k = 0
    )
    )
    print(f"[INFO] Gemini output:\n{response.text}")
    code = "\n".join(response.text.split('\n')[1:-1])
    return code

def fetch_and_generate_prompt(file_path):
    """
    Fetches news articles and generates a prompt for the Gemini API.
    """
    # Step 1: Fetch the latest news
    articles = fetch_news()
    if not articles:
        print("[INFO] No new articles fetched. Exiting.")
        return None

    # Step 2: Create a prompt for Gemini
    with open(file_path, 'r') as file:
        file_content = file.read()
    prompt = f"""
        Write a test class for the following file. Only include checks to see if its code 
        is compliant with the regulatory changes described in the news 
        context below. Make sure that the test class name and package match the names in the file.
        Write at least 3 tests.
        In the test methods, also include two println statements:
        1. The test name and the cause for which this test case would fail 
        2. The test name and possible remediations in case that test fails
        Reply only with complete code and no other explanations. Try your best to make test cases that would fail. 
        '''
        {file_content}
        '''
        News Context:\n
    """ + "\n".join(articles)
    print(f"[INFO] Generated Prompt:\n{prompt}")
    return prompt

def create_test_file(file_path, src_directory, generated_test):
    """
    Creates a test file with the generated test code.
    """
    test_file_path = file_path.replace("main", "test").replace(".java", "Test.java")
    test_file_directory = os.path.join(src_directory, "src", "test", "java")
    os.makedirs(test_file_directory, exist_ok=True)  # Ensure the test directory exists

    # Generate class name from test_file_path
    relative_path = os.path.relpath(test_file_path, start=test_file_directory)
    class_name = ".".join(relative_path.split(os.sep))
    class_name = ".".join(class_name.split(".")[:-1])  # Remove the .java extension

    print(f"[INFO] Relative Path: {relative_path}")
    print(f"[INFO] Generated Class Name: {class_name}")

    # # Replace placeholder in generated test code with the class name
    # if "{class_name}" in generated_test:
    #     generated_test = generated_test.replace("{class_name}", class_name)

    with open(test_file_path, 'w') as test_file:
        test_file.write(generated_test)
    print(f"[INFO] Test file created at: {test_file_path}")
    return test_file_path, class_name

def run_gradle_tests(class_name, project_directory):
    """
    Runs Gradle tests for the specified class.
    """
    gradle_command = f"gradle test --tests {class_name}"
    print(f"[INFO] {gradle_command}")
    try:
        result = subprocess.run(
            gradle_command.split(" "),
            cwd=project_directory,
            capture_output=True,
            text=True,
            check=True
        )
        print("[INFO] Gradle Test Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("[ERROR] Error running Gradle tests:")
        print(e.stderr)
        return 
    return 

def delete_test_file(test_file_path):
    """
    Deletes the created test file.
    """
    try:
        os.remove(test_file_path)
        print(f"[INFO] Deleted test file: {test_file_path}")
    except OSError as e:
        print(f"[ERROR] Failed to delete test file: {e}")


def launch_test_report(gradle_directory):
    """
    Launches the test report in the default browser.
    """
    report_path = os.path.join(gradle_directory, "app", "build", "reports", "tests", "test", "index.html")
    if os.path.exists(report_path):
        print(f"[INFO] Test report available at: {report_path}")
        
        if sys.platform == "win32":
            os.startfile(report_path)  # Windows
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", report_path])
        else:  # Linux and others
            subprocess.run(["xdg-open", report_path])
    else:
        print("[INFO] Test report not found.")

def launch_test_viewer(generated_test, test_name):
    """
    Converts the generated test code into an HTML file and opens it in the default browser.
    """
    # Convert the generated test code to HTML using java_to_html
    
    # Create the HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Code</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/default.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', (event) => {{
            document.querySelectorAll('pre code').forEach((block) => {{
                hljs.highlightElement(block);
            }});
        }});
    </script>
    <style>
        h1 {{
            font-size: 25.6px;
            font-family: sans-serif;
        }}
    </style>
</head>
<body>
    <h1>{test_name}</h1>
    <pre><code class="language-java">
{generated_test}
    </code></pre>
</body>
</html>"""

    # Save the HTML content to a file
    html_file_path = "generated_test.html"
    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)
    
    print(f"[INFO] Test viewer HTML file created at: {html_file_path}")
    
    # Open the HTML file in the default browser
    webbrowser.open(f"file://{os.path.abspath(html_file_path)}")

# Update run_glue to call launch_test_viewer
def run_glue(file_path):
    """
    Executes the following steps:
    1. Calls fetch_news to get the latest news.
    2. Creates a prompt for Gemini using the fetched news and file content.
    3. Runs Gradle tests for the newly created test file.
    4. Launches the test report.
    5. Creates a test file with the generated test code.
    6. Launches the test viewer to display the generated test code.
    """
    gradle_directory = find_gradle_root(file_path)
    src_directory = find_src_root(file_path)
    print(f"[INFO] Gradle Directory: {gradle_directory}")
    print(f"[INFO] Source Directory: {src_directory}")

    # run_news_api_as_process()
    # Step 1 & 2: Fetch news and generate prompt
    prompt = fetch_and_generate_prompt(file_path)
    if not prompt:
        return

    # Step 3: Call Gemini API to generate the test code
    generated_test = do_inference(prompt)
    if not generated_test:
        print("[INFO] No test code generated. Exiting.")
        return

    # Step 4: Create a test file with the generated test code
    test_file_path, class_name = create_test_file(file_path, src_directory, generated_test)

    # Step 5: Run Gradle tests for the newly created test file
    run_gradle_tests(class_name, gradle_directory)
    
    # Step 6: Launch the test report
    launch_test_report(gradle_directory)

    # Step 7: Launch the test viewer to display the generated test code
    launch_test_viewer(generated_test, class_name)

    # Step 8: Delete the created test file
    delete_test_file(test_file_path)
    
def find_gradle_root(file_path):
    """
    Searches the ancestor directories of the given file path until it finds a directory
    containing a .gradle directory.

    :param file_path: The file path to start the search from.
    :return: The path to the directory containing the .gradle directory, or None if not found.
    """
    current_dir = os.path.abspath(file_path)

    while current_dir != os.path.dirname(current_dir):  # Stop when reaching the root directory
        gradle_dir = os.path.join(current_dir, ".gradle")
        if os.path.isdir(gradle_dir):
            print(f"[INFO] Found .gradle directory at: {current_dir}")
            return current_dir
        current_dir = os.path.dirname(current_dir)  # Move to the parent directory

    print("[INFO] .gradle directory not found in any ancestor directories.")
    return None

def find_src_root(file_path):
    """
    Searches the ancestor directories of the given file path until it finds a directory
    containing a 'src' folder.

    :param file_path: The file path to start the search from.
    :return: The path to the directory containing the 'src' folder, or None if not found.
    """
    current_dir = os.path.abspath(file_path)

    while current_dir != os.path.dirname(current_dir):  # Stop when reaching the root directory
        src_dir = os.path.join(current_dir, "src")
        if os.path.isdir(src_dir):
            print(f"[INFO] Found 'src' directory at: {current_dir}")
            return current_dir
        current_dir = os.path.dirname(current_dir)  # Move to the parent directory

    print("[INFO] 'src' directory not found in any ancestor directories.")
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the glue script with a specified file path.")
    parser.add_argument(
        "file_path",
        type=str,
        help="The path to the Java file for which tests will be generated."
    )
    args = parser.parse_args()

    run_glue(args.file_path)

