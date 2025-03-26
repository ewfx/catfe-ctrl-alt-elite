import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini API key
GEMINI_API_KEY = os.getenv("AIzaSyDY0vUYOaL145J-EGlLDH2cHDeaxrdsr5Q")

# Initialize API with the correct key
genai.configure(api_key=GEMINI_API_KEY)

# List available models
available_models = genai.list_models()

print("Available Models:")
for model in available_models:
    print(f"- {model.name}")
