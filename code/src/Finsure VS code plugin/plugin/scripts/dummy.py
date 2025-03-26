import sys
import streamlit as st

# Force UTF-8 encoding to avoid Windows UnicodeEncodeError
sys.stdout.reconfigure(encoding="utf-8")

st.title("Simple Streamlit Frontend")
st.write("This is a basic Streamlit app.")

name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello, {name}!")

number = st.slider("Pick a number", 1, 100, 50)
st.write(f"You selected: {number}")

if st.button("Click Me"):
    st.success("Button clicked!")

# Get input from command-line arguments
if len(sys.argv) < 2:
    print("❌ No input provided. Select text or right-click on a file.")
    sys.exit(1)

# Retrieve the content and restore newlines
input_content = sys.argv[1].replace("\\n", "\n")

# Display the content
st.write("### 📄 Content:")
st.code(input_content, language="plaintext")