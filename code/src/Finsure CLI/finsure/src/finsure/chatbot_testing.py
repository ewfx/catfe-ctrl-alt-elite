import streamlit as st
import subprocess
import sys
import os

# Hardcoded paths
GENERATE_SCRIPT = "/Users/Jyothikamalesh/Projects/testing tool/finsure/src/finsure/generate_testcases.py"
TEST_SCRIPT = "/Users/Jyothikamalesh/Projects/testing tool/finsure/src/finsure/test_chatbot.py"
TEMP_FILE = "/Users/Jyothikamalesh/Projects/testing tool/finsure/src/finsure/temp_testcases.txt"

def generate_chatbot_testcases(url):
    command = [sys.executable, GENERATE_SCRIPT, url]  # Hardcoded path
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", text=True, bufsize=1)
    output = "".join(iter(process.stdout.readline, ""))
    process.stdout.close()
    process.wait()

    test_cases = output.split("📄 Generated Chatbot Injection Test Cases:\n")[-1].strip()
    return test_cases

def test_chatbot(url, test_cases):
    with open(TEMP_FILE, "w", encoding="utf-8") as f:
        f.write(test_cases)
    
    command = [sys.executable, TEST_SCRIPT, url, TEMP_FILE]  # Hardcoded path
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", text=True, bufsize=1)
    output = "".join(iter(process.stdout.readline, ""))
    process.stdout.close()
    process.wait()
    
    return output.strip()

def main():
    st.title("Chatbot Automation Testing")
    
    chatbot_url = st.text_input("Enter Chatbot URL:", key="chatbot_url")
    
    if 'test_cases' not in st.session_state:
        st.session_state.test_cases = ""
    
    if st.button("Generate Test Cases", key="generate_testcases"):
        if chatbot_url:
            st.info("Generating Test Cases...")
            test_cases = generate_chatbot_testcases(chatbot_url)
            st.session_state.test_cases = test_cases
            st.text_area("Generated Test Cases:", test_cases, height=200)
            st.success("Test Cases Generated!")
        else:
            st.error("Please provide a Chatbot URL.")
    
    if st.button("Test Chatbot", key="test_chatbot"):
        if chatbot_url:
            if not st.session_state.test_cases:
                st.error("Please generate test cases first.")
                return
                
            st.info("Testing Chatbot...")
            test_results = test_chatbot(chatbot_url, st.session_state.test_cases)
            st.text_area("Test Results:", test_results, height=200)
            st.success("Chatbot Testing Completed!")
        else:
            st.error("Please provide a Chatbot URL.")

    st.markdown("---")

if __name__ == "__main__":
    main()
