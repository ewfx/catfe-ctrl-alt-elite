# paypal_config.py
import paypalrestsdk
import os
# Configure PayPal directly in this file
paypalrestsdk.configure({
    "mode": "sandbox",  # 'sandbox' for testing or 'live' for production
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET"),
})
