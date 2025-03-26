import streamlit as st
import subprocess
import sys
import os

# Ensure the script finds generate_testcases.py in the correct directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TESTCASE_SCRIPT = os.path.join(BASE_DIR, "generate_testcases.py")
TEST_SCRIPT = os.path.join(BASE_DIR, "test_chatbot.py")

def generate_chatbot_testcases(url):
    if not os.path.exists(TESTCASE_SCRIPT):
        return f"Error: {TESTCASE_SCRIPT} not found."

    command = [sys.executable, TESTCASE_SCRIPT, url]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", text=True, bufsize=1)
    
    output = ""
    for line in iter(process.stdout.readline, ""):
        output += line + "\n"
    process.stdout.close()
    process.wait()
    return output.strip()

def test_chatbot(url):
    if not os.path.exists(TEST_SCRIPT):
        return f"Error: {TEST_SCRIPT} not found."

    command = [sys.executable, TEST_SCRIPT, url]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", text=True, bufsize=1)
    
    output = ""
    for line in iter(process.stdout.readline, ""):
        output += line + "\n"
    process.stdout.close()
    process.wait()
    return output.strip()

def main():
    st.title("Chatbot Automation Testing")
       
    chatbot_url = st.text_input("Enter Chatbot URL:", key="chatbot_url")
    
    if st.button("Generate Test Cases", key="generate_testcases"):
        if chatbot_url:
            st.info("Generating Test Cases...")
            test_cases = generate_chatbot_testcases(chatbot_url)
            st.text_area("Generated Test Cases:", test_cases, height=200)
            st.success("Test Cases Generated!")
        else:
            st.error("Please provide a Chatbot URL.")
    
    if st.button("Test Chatbot", key="test_chatbot"):
        if chatbot_url:
            st.info("Testing Chatbot...")
            test_results = test_chatbot(chatbot_url)
            st.text_area("Test Results:", test_results, height=200)
            st.success("Chatbot Testing Completed!")
        else:
            st.error("Please provide a Chatbot URL.")

    st.markdown("---")

if __name__ == "__main__":
    main()
