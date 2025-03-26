import json
import os
import re
import logging
import google.generativeai as genai
import requests
import sys

from dotenv import load_dotenv
from pathlib import Path

TEST_CASES_DIR = "/app/src/"




GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logging.critical("❗️ GEMINI_API_KEY is not set. Check your .env file.")
    raise ValueError("GEMINI_API_KEY is not set. Check your .env file.")

genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-1.5-flash"
# PAYMENT_API_URL = "http://localhost:8001/process_payment/"
PAYMENT_API_URL = "http://mock_api:8001/process_payment/"


log_file = os.path.join(TEST_CASES_DIR, "test_execution.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("🚀 Script execution started.")
logging.info("✅ Environment variables loaded successfully.")
logging.info("⚡️ API configured with model: %s", MODEL_NAME)


def clean_response(response_text):
    """Cleans and validates AI response to ensure proper JSON format."""
    logging.info("🔍 Cleaning and validating AI response...")
    try:
        response_text = response_text.replace("```json", "").replace("```", "").strip()

        response_text = re.sub(r'//.*?$', '', response_text, flags=re.MULTILINE)
        response_text = re.sub(r',\s*([\]}])', r'\1', response_text)

        json_data = json.loads(response_text)
        logging.info("✅ AI response cleaned successfully.")
        return json.dumps(json_data, indent=4)

    except json.JSONDecodeError as e:
        logging.error(f"❌ Invalid JSON format in AI response. Error: {e}")
        raise ValueError(f"Invalid JSON format. Unable to parse: {response_text}\nError: {e}")


def generate_test_cases():
    """Generate test cases for SWIFT, FED, and CHIPS compliance using Gemini AI."""
    logging.info("⚡️ Generating test cases using Gemini AI...")

  
    system_prompt = (
        "You are an expert in financial transaction testing. "
        "Generate diverse test cases covering SWIFT ISO 20022, FED, and CHIPS compliance scenarios. "
        "Each test case must include a valid scenario, input data, expected output, and status."
    )

    user_prompt = """
    Generate structured JSON test cases for:
    1. SWIFT ISO 20022: Valid and invalid transactions.
    2. FEDWIRE compliance: Successful and rejected payments.
    3. CHIPS transactions: Fraud detection and payment validation.

    Each test case must follow this format:
    ```json
    {
      "test_cases": [
        {
          "id": 1,
          "scenario": "Valid SWIFT ISO 20022 Transaction",
          "input_data": {
            "amount": 1000.00,
            "currency": "USD",
            "payment_method": "paypal"
          },
          "expected_output": {
            "status": "success",
            "approval_url": "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token=..."
          }
        },
        {
          "id": 2,
          "scenario": "FEDWIRE Payment - Insufficient Funds",
          "input_data": {
            "amount": 2000000.00,
            "currency": "USD",
            "payment_method": "paypal"
          },
          "expected_output": {
            "status": "error",
            "error": "Insufficient Funds"
          }
        }
      ]
    }
    ```
    """

    try:
       
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content([system_prompt, user_prompt])

        generated_text = response.text.strip()
        logging.info("✅ Test cases generated by Gemini AI. Cleaning response...")

        cleaned_text = clean_response(generated_text)

        test_cases = json.loads(cleaned_text)
        output_file = os.path.join(TEST_CASES_DIR, "sample_test.json")

        with open(output_file, "w") as f:
            json.dump(test_cases, f, indent=4)

        logging.info(f"📂 Test cases saved in {output_file}")
        return test_cases

    except Exception as e:
        logging.error(f"❌ Error generating test cases: {e}")
        raise ValueError(f"Error generating test cases: {e}")
    
def generate_test_cases_from_file(file_content):
    """Generates test cases dynamically based on uploaded file content."""
    logging.info("📄 Generating test cases dynamically from uploaded file content...")

    if not isinstance(file_content, str):
        try:
            file_content = file_content.decode("utf-8")  
        except UnicodeDecodeError:
            logging.error("❌ Error decoding file content. Ensure it's a text-based format.")
            raise ValueError("File content is not a valid text format.")

    system_prompt = (
        "You are an expert in financial transaction testing. "
        "Analyze the provided file content and generate structured test cases covering "
        "SWIFT ISO 20022, FEDWIRE, and CHIPS compliance scenarios. "
        "Each test case must include a valid scenario, input data, expected output, and status."
    )
    user_prompt = f"""
    Given the following file content:
    ```
    {file_content}
    ```
    Generate structured JSON test cases for:
    1. SWIFT ISO 20022: Valid and invalid transactions.
    2. FEDWIRE compliance: Successful and rejected payments.
    3. CHIPS transactions: Fraud detection and payment validation.

    Each test case must follow this format:
    ```json
    {{
      "test_cases": [
        {{
          "id": 1,
          "scenario": "Valid SWIFT ISO 20022 Transaction",
          "input_data": {{
            "amount": 1000.00,
            "currency": "USD",
            "payment_method": "paypal"
          }},
          "expected_output": {{
            "status": "success",
            "approval_url": "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token=..."
          }}
        }},
        {{
          "id": 2,
          "scenario": "FEDWIRE Payment - Insufficient Funds",
          "input_data": {{
            "amount": 2000000.00,
            "currency": "USD",
            "payment_method": "paypal"
          }},
          "expected_output": {{
            "status": "error",
            "error": "Insufficient Funds"
          }}
        }}
      ]
    }}
    ```
    """

    try:
    
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content([system_prompt, user_prompt])

        generated_text = response.text.strip()
        logging.info("✅ Test cases generated from file. Cleaning response...")

        cleaned_text = clean_response(generated_text)

        test_cases = json.loads(cleaned_text)
        output_file = os.path.join(TEST_CASES_DIR, "dynamic_test_cases.json")

        with open(output_file, "w") as f:
            json.dump(test_cases, f, indent=4)

        logging.info(f"📂 Dynamic test cases saved in {output_file}")
        return test_cases

    except Exception as e:
        logging.error(f"❌ Error generating test cases from file: {e}")
        raise ValueError(f"Error generating test cases from file: {e}")


def convert_to_paypal_format(input_data):
    try:
        if "MsgType" in input_data and input_data["MsgType"] == "pacs.008":
            return {
                "amount": float(input_data["CdtTrfTxInf"]["Amt"]["InstdAmt"].get("value", 0)),  # Default value 0
                "currency": input_data["CdtTrfTxInf"]["Amt"]["InstdAmt"].get("Ccy", "USD"),  # Default currency
                "payment_method": "paypal",
                "description": f"SWIFT ISO 20022 Transaction {input_data.get('MsgId', 'UNKNOWN')}"
            }

        elif "paymentType" in input_data and input_data["paymentType"] == "FEDWIRE":
           
            return {
                "amount": float(input_data.get("amount", 0)),  # Default amount 0
                "currency": "USD",
                "payment_method": "paypal",
                "description": f"FEDWIRE Payment {input_data.get('routingNumber', 'UNKNOWN_ROUTING')}"
            }

        elif "paymentType" in input_data and input_data["paymentType"] == "CHIPS":
            return {
                "amount": float(input_data.get("amount", 0)),  # Default amount 0
                "currency": "USD",
                "payment_method": "paypal",
                "description": f"CHIPS Transaction {input_data.get('transactionId', 'UNKNOWN_TRANSACTION')}"
            }

        else:
            logging.warning("⚠️ Unknown payment type. Defaulting to generic PayPal transaction.")
            return {
                "amount": 10.00,  # Default small amount
                "currency": "USD",
                "payment_method": "paypal",
                "description": "Default Payment"
            }

    except KeyError as e:
        logging.error(f"Missing key in input data: {e}")
        raise ValueError(f"Missing key in input data: {e}")

    except Exception as e:
        logging.error(f"Error converting to PayPal format: {e}")
        raise ValueError(f"Error converting to PayPal format: {e}")
    
def generate_fraud_test_cases():
    """Generate fraud-specific test cases using Gemini AI."""
    logging.info("⚡️ Generating fraud detection test cases...")

    user_prompt = """
    Generate structured JSON fraud test cases for:
    1. Transaction structuring (Splitting large payments).
    2. Synthetic identity fraud (Fake accounts).
    3. Account takeover fraud (New device/IP usage).
    4. Money laundering patterns (High-volume circular transactions).

    Each test case must follow this format:
    ```json
    {
      "id": 101,
      "scenario": "Fraudulent transaction - Account Takeover",
      "input_data": {
        "amount": 9000.00,
        "currency": "USD",
        "payment_method": "paypal",
        "location": "Russia",
        "user_ip": "203.0.113.45"
      },
      "expected_output": {
        "status": "flagged",
        "reason_code": "ACCOUNT_TAKEOVER",
        "fraud_score": 0.92
      }
    }
    ```
    """

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content([user_prompt])

        generated_text = response.text.strip()
        cleaned_text = clean_response(generated_text)

        fraud_test_cases = json.loads(cleaned_text)
        output_file = os.path.join(TEST_CASES_DIR, "fraud_test_cases.json")

        with open(output_file, "w") as f:
            json.dump(fraud_test_cases, f, indent=4)

        logging.info(f"📂 Fraud test cases saved in {output_file}")
        return fraud_test_cases

    except Exception as e:
        logging.error(f" Error generating fraud test cases: {e}")
        raise ValueError(f"Error generating fraud test cases: {e}")
    

def run_test_cases(test_cases, file_data=None):
    """Run generated test cases and validate responses with the mock API."""
    logging.info("🧪 Running generated test cases...")
    results = []

    for test in test_cases["test_cases"]:
        scenario = test["scenario"]
        input_data = test["input_data"]

        payload = convert_to_paypal_format(input_data)

        logging.info(f"🚀 Sending request to mock API for scenario: {scenario}")
        logging.info(f"Payload: {json.dumps(payload, indent=4)}")

        try:
          
            response = requests.post(PAYMENT_API_URL, json=payload, timeout=10)
            response.raise_for_status()

            if response.status_code == 200:
                result = response.json()
                status = "pass" if result["status"] == test["expected_output"]["status"] else "fail"
                logging.info(f"✅ Response received for test {test['id']}: {json.dumps(result, indent=4)} | Status: {status}")
            else:
                status = "fail"
                result = {"error": f"API returned status code {response.status_code}"}
                logging.error(f"API error: {result['error']}")

        except requests.RequestException as e:
            status = "error"
            result = {"error": f"API connection failed: {str(e)}"}
            logging.error(f"❌ Error running test case {test['id']}: {e}")

        results.append({
            "id": test["id"],
            "scenario": scenario,
            "status": status,
            "expected_output": test["expected_output"],
            "actual_response": result,
        })

    result_file = os.path.join(TEST_CASES_DIR, "test_results.json")
    try:
        with open(result_file, "w") as f:
            json.dump(results, f, indent=4)
        logging.info(f"Test results saved in {result_file}")
    except IOError as e:
        logging.error(f"❌ Error saving test results: {e}")
        raise IOError(f"Error saving test results: {e}")

    logging.info("✅ Test case execution completed.")
    return results

if __name__ == "__main__":
    logging.info("⚡️ Starting test case generation and execution...")

    # Generate and run test cases
    try:
        test_cases = generate_test_cases()
        test_results = run_test_cases(test_cases)
        logging.info("🎉 Test case execution completed successfully.")
        print(f"✅ Test cases completed. Results saved in {TEST_CASES_DIR}/test_results.json")

    except Exception as e:
        logging.error(f"❌ Error during execution: {e}")
        print(f"❌ Error during execution: {e}")
