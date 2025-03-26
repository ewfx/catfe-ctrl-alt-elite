import os
import sys
import subprocess
import streamlit as st

# Get the correct path to `browser_automation.py`
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.join(BASE_DIR, "browser_automation.py")

def run_script(url, user_prompt):
    if not os.path.exists(SCRIPT_PATH):
        st.error(f"Error: {SCRIPT_PATH} not found.")
        return
    
    command = [sys.executable, SCRIPT_PATH, url, user_prompt]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", text=True, bufsize=1)

    try:
        for line in iter(process.stdout.readline, ""):
            yield line.strip()
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        process.terminate()
        process.stdout.close()
        process.wait()

def main():
    st.title("UI Automation Testing")

    url = st.text_input("Enter URL:")
    user_prompt = st.text_area("Enter User Prompt:")

    if st.button("Submit"):
        if url and user_prompt:
            st.info("Starting UI Testing Automation...")
            log_area = st.empty()

            with log_area.container():
                for log in run_script(url, user_prompt):
                    st.write(log)

            st.success("UI Automation Completed!")
        else:
            st.error("Please provide both URL and User Prompt.")

if __name__ == "__main__":
    main()
