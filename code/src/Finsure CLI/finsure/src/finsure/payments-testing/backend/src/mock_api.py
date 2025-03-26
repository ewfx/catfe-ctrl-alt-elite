from fastapi import FastAPI, Body
import paypal_config
import paypalrestsdk
from paypalrestsdk import Payment
import logging
import time

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Simulated transaction history for fraud detection
transaction_history = {}

def detect_fraud_or_compliance(input_data):
    """Detect fraud patterns and compliance violations before processing payment."""
    fraud_score = 0  # Start with a neutral score

    user_id = input_data.get("user_id", "unknown")
    amount = float(input_data.get("amount", 0))
    currency = input_data.get("currency", "USD")
    location = input_data.get("location", "unknown")
    user_ip = input_data.get("user_ip", "0.0.0.0")
    payment_method = input_data.get("payment_method", "paypal")

    # Ensure transaction history exists for user
    if user_id not in transaction_history:
        transaction_history[user_id] = []

    
    if amount > 100000:
        fraud_score += 0.5

  
    previous_locations = [tx["location"] for tx in transaction_history[user_id]]
    if location not in previous_locations and len(previous_locations) > 2:
        fraud_score += 0.3

    timestamps = [tx["timestamp"] for tx in transaction_history[user_id]]
    if len(timestamps) >= 3 and (time.time() - timestamps[-3]) < 300:  # 3 transactions in <5 min
        fraud_score += 0.4

    if len(transaction_history[user_id]) < 3 and amount > 50000:
        fraud_score += 0.3

    
    transaction_history[user_id].append({
        "amount": amount,
        "currency": currency,
        "location": location,
        "user_ip": user_ip,
        "timestamp": time.time()
    })

    
    if fraud_score > 0.7:
        logging.warning(f"🚨 High fraud score detected for user {user_id}: {fraud_score}")
        return {
            "status": "error",
            "message": "Fraud detection triggered. Payment blocked.",
            # "fraud_score": round(fraud_score, 2)
        }

    return None  # 

def process_paypal_payment(input_data):
    """Send transaction to PayPal if it passes fraud detection."""
    logging.info(f"✅ Sending payment to PayPal: {input_data}")

    if input_data["amount"] > 1000000:  # Reject transactions > $1M
        return {"status": "error", "error": "Insufficient Funds"}

    if input_data["currency"] not in ["USD", "EUR", "GBP"]:  # Reject unsupported currencies
        return {"status": "error", "error": "Unsupported Currency"}

    payment = Payment({
        "intent": "sale",
        "payer": {"payment_method": input_data["payment_method"]},
        "transactions": [{"amount": {"total": str(input_data["amount"]), "currency": input_data["currency"]}}],
        "redirect_urls": {"return_url": "http://localhost:8001/payment/success", "cancel_url": "http://localhost:8001/payment/cancel"}
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return {"status": "success", "approval_url": link.href}
        return {"status": "error", "message": "No approval_url found."}

    logging.error(f"❌ PayPal API Error: {payment.error}")
    return {"status": "error", "error": payment.error}

@app.post("/process_payment/")
async def process_payment(input_data: dict = Body(...)):
    """Intercept payment requests and check for fraud before sending to PayPal."""
    logging.info(f"🔍 Processing Payment - Input: {input_data}")

    fraud_result = detect_fraud_or_compliance(input_data)
    if fraud_result:
        logging.warning(f"🚨 Fraud detected: {fraud_result}")
        return fraud_result  # 🚫 Stop processing

    return process_paypal_payment(input_data)
