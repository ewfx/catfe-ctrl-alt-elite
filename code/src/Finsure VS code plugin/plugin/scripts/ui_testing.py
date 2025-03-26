import streamlit as st
import subprocess
import sys
import time

def run_script(url, user_prompt):
    command = [sys.executable, "./scripts/ui_test/browser_automation.py", url, user_prompt]
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

    # st.header("UI Testing")
    url = st.text_input("Enter URL:", key="ui_url")
    user_prompt = st.text_area("Enter User Prompt:", key="ui_prompt")
    if st.button("Submit", key="ui_submit"):
        if url and user_prompt:
            st.info("Starting UI Testing Automation...")
            log_area = st.empty()
            with log_area.container():
                for log in run_script(url, user_prompt):
                    st.write(log)
            st.success("UI Automation Completed!")
        else:
            st.error("Please provide both URL and User Prompt.")
    
    st.markdown("---")

if __name__ == "__main__":
    port = 8503
    sys.argv = ["streamlit", "run", __file__, "--server.port", str(port)]
    main()
    
# import streamlit as st
# import subprocess
# import sys
# import time

# def run_script(url, user_prompt):
#     command = [sys.executable, "browser_automation.py", url, user_prompt]
#     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", text=True, bufsize=1)

#     try:
#         for line in iter(process.stdout.readline, ""):
#             yield line.strip()
#     except Exception as e:
#         st.error(f"Error: {e}")
#     finally:
#         process.terminate()  # Ensure process is killed when session ends
#         process.stdout.close()
#         process.wait()

# def main():
#     st.title("Browser Automation with Streamlit")

#     url = st.text_input("Enter URL:")
#     user_prompt = st.text_area("Enter User Prompt:")

#     if st.button("Submit"):
#         if url and user_prompt:
#             st.info("Starting Automation...")
#             log_area = st.empty()

#             with log_area.container():
#                 for log in run_script(url, user_prompt):
#                     st.write(log)

#             st.success("Automation Completed!")
#         else:
#             st.error("Please provide both URL and User Prompt.")

# if __name__ == "__main__":
#     main()
