import os
from dotenv import load_dotenv

load_dotenv()
 
# Base directory for storing test cases
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory where test cases will be stored
TEST_CASES_DIR = os.path.join(BASE_DIR, "src", "test_cases")

# Ensure the directory exists
os.makedirs(TEST_CASES_DIR, exist_ok=True)

