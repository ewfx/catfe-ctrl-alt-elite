import os
import asyncio
import sys
import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser

# Setup logging to console only
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Ensure stdout uses UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logging.error("❌ GEMINI_API_KEY is missing! Add it to your .env file.")
    sys.exit(1)

logging.info("✅ API Key Loaded Successfully.")

# Read URL and User Prompt from command-line arguments
if len(sys.argv) < 3:
    logging.error("❌ Usage: python browser-automation.py <URL> <USER_PROMPT>")
    sys.exit(1)

url = sys.argv[1]
user_prompt = sys.argv[2]

logging.info(f"🌐 Starting automation for URL: {url}")
logging.info(f"📝 User Prompt: {user_prompt}")

# Create a dynamic task
task = f"""
### Automated Test Execution

**Objective:**  
Visit [{url}]({url}) and execute the following test based on the user's instructions.

**Test Instructions:**  
{user_prompt}

**Steps to Perform:**
1. Open the website: {url}.
2. Follow the steps described in the user prompt.
3. Capture any relevant output or errors encountered.
4. Provide a summary of actions taken.

**Expected Output:**  
- Details of actions performed  
- Any errors encountered  
- Confirmation if the test was successful
"""

logging.debug("🚀 Task created for execution.")

# Initialize the browser and agent
try:
    browser = Browser()
    agent = Agent(
        task=task,
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key),
        browser=browser,
    )
    logging.info("✅ Browser and Agent initialized successfully.")
except Exception as e:
    logging.error(f"❌ Failed to initialize Browser or Agent: {e}", exc_info=True)
    sys.exit(1)

async def main():
    try:
        logging.info("🔄 Running automation task...")
        await agent.run()
        logging.info("✅ Automation completed successfully.")
    except Exception as e:
        logging.error(f"❌ Automation failed: {e}", exc_info=True)
    finally:
        logging.info("🔄 Closing browser...")
        await browser.close()
        logging.info("🛑 Browser closed.")

if __name__ == '__main__':
    logging.info("📌 Starting automation script...")
    asyncio.run(main())
    logging.info("📌 Script execution finished.")