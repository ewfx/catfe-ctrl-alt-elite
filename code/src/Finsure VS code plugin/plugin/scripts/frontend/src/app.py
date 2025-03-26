import streamlit as st
import json
import os
import requests
import google.generativeai as genai
import pandas as pd
from test_generator import generate_test_cases, generate_test_cases_from_file, run_test_cases
from fpdf import FPDF
import subprocess
# from st_aggrid import AgGrid, GridOptionsBuilder

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-1.5-flash"

st.title("Payment Gateway API Testing")

st.text_input("API Endpoint URL", placeholder="Enter the API endpoint URL here...", disabled=False)
st.text_input("API Key", placeholder="Enter your API key here...", type="password", disabled=False)


if "test_cases" not in st.session_state:
    st.session_state["test_cases"] = None
if "test_results" not in st.session_state:
    st.session_state["test_results"] = None
if "file_content" not in st.session_state:
    st.session_state["file_content"] = None


def analyze_test_results_with_ai(test_results):
    user_prompt = f"""
    Analyze the following test results and provide insights:

    {json.dumps(test_results, indent=4)}

    - Identify why tests failed.
    - Suggest possible resolutions.
    - Highlight fraud concerns if applicable.
    - Provide a structured, professional response.
    """
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content([user_prompt])
    return response.text.strip()


def display_test_results(results):
    df = pd.DataFrame(results)
    df["Status"] = df["status"].apply(lambda x: f"✔️ PASS" if x == "pass" else f"❌ FAIL")
    df["Expected Output"] = df["expected_output"].apply(lambda x: json.dumps(x, indent=2))
    df["Actual Response"] = df["actual_response"].apply(lambda x: json.dumps(x, indent=2))
    df = df[["id", "scenario", "Status", "Expected Output", "Actual Response"]]
    st.dataframe(df)


# if st.button("🛠 Generate and Run Test Cases"):
#     with st.spinner("Generating Test Cases..."):
#         try:
#             test_cases = generate_test_cases()
#             st.session_state["test_cases"] = test_cases
#             st.success("✅ Test Cases Generated Successfully!")

#             st.markdown("### Generated Test Cases")
#             st.json(test_cases)

#             with st.spinner("Running Payment Tests..."):
#                 results = run_test_cases(test_cases)
#                 st.session_state["test_results"] = results
#                 st.success("✅ Payment Tests Completed!")
#                 display_test_results(results)

#                 with st.spinner("Analyzing Test Failures..."):
#                     ai_analysis = analyze_test_results_with_ai(results)
#                     st.write("### Analysis & Fixes")
#                     st.markdown(ai_analysis)

#         except Exception as e:
#             st.error(f"❌ Error: {e}")

# ✅ File Upload for Custom Test Cases
uploaded_file = st.file_uploader("", type=["json", "txt"])

# ✅ Export to PDF with Test Cases Persistence
def export_to_pdf():
    if st.session_state["test_cases"] and st.session_state["test_results"]:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Payment Gateway API Testing Report", ln=True, align="C")

        def add_section(title, content):
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, title, ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 8, content.encode('latin-1', 'replace').decode('latin-1'))

        add_section("Uploaded File Content", st.session_state.get("file_content", "N/A"))
        add_section("Generated Test Cases", json.dumps(st.session_state["test_cases"], indent=2))
        add_section("Test Execution Details", json.dumps(st.session_state["test_results"], indent=2))

        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "AI-Generated Analysis & Fixes", ln=True)
        pdf.set_font("Arial", "", 10)
        ai_analysis = analyze_test_results_with_ai(st.session_state["test_results"])
        pdf.multi_cell(0, 8, ai_analysis.encode('latin-1', 'replace').decode('latin-1'))

        pdf_output = "payment_testing_report.pdf"
        pdf.output(pdf_output, "F")

        # ✅ Open the generated PDF and prepare for download without modifying session state
        with open(pdf_output, "rb") as file:
            st.download_button(
                "📥 Export Report as PDF",
                file,
                file_name=pdf_output,
                mime="application/pdf",
                key="download_pdf"  # ✅ Adding a unique key to prevent re-rendering
            )
               

if "report_ready" not in st.session_state:
    st.session_state["report_ready"] = False
    



if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
    st.session_state["file_content"] = file_content
    st.write("✅ File Uploaded Successfully!")

    if st.button("Generate Tests"):
        with st.spinner("Processing file..."):
            try:
                test_cases = generate_test_cases_from_file(file_content)
                st.session_state["test_cases"] = test_cases
                st.session_state["report_ready"] = True
                st.success("✅ Test Cases Generated!")

                st.markdown("### Generated Test Cases")
                st.json(test_cases)

                with st.spinner("Running Tests..."):
                    results = run_test_cases(test_cases)
                    st.session_state["test_results"] = results
                    st.success("✅ Tests Completed!")
                    display_test_results(results)

                    with st.spinner("Analyzing Test Failures..."):
                        ai_analysis = analyze_test_results_with_ai(results)
                        st.write("### Analysis & Fixes")
                        st.markdown(ai_analysis)

            except Exception as e:
                st.error(f"❌ Error processing file: {e}")

if st.session_state["report_ready"]:
    export_to_pdf()


# if st.button("KIll docker"):
#     with st.spinner("Stopping Docker..."):
#         stop_docker()