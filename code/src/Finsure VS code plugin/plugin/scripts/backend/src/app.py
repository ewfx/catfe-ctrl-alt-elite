import paypalrestsdk
from fastapi import FastAPI
from paypalrestsdk import Payment

app = FastAPI()

paypalrestsdk.configure({
    "mode": "sandbox", 
    "client_id": "ATN3u3-kpky0ncex7XIenzhtB4JYSnPGs9XrEuYc4cNh6vJ1QE9NAwXtFzx9yaJzoJQ6D63QGJGxDLjB",
    "client_secret": "EIITqNpmnfYQtJd7iOiWGb8g-jrYvnbziJj1nLdW9tMP17Zb8WNUFO_3nYZa2dUqNcfkikqhCRZJrTj3",
})

PAYEE_EMAIL = "sb-laidz38109996@business.example.com"  


@app.post("/process_payment/")
async def process_payment(amount: float, currency: str, payment_method: str = "paypal"):
    """
    Process payment through PayPal Sandbox API.
    
    :param amount: Amount to be paid.
    :param currency: Currency of payment.
    :param payment_method: Either 'paypal' or 'credit_card'.
    """
    try:
        if payment_method == "credit_card":
            payment = Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "credit_card",
                    "funding_instruments": [{
                        "credit_card": {
                            "type": "visa",
                            "number": "4111111111111111",
                            "expire_month": "12",
                            "expire_year": "2026",
                            "cvv2": "123",
                            "first_name": "John",
                            "last_name": "Doe"
                        }
                    }]
                },
                "transactions": [
                    {
                        "amount": {
                            "total": str(amount),
                            "currency": currency
                        },
                        "description": "Payment Simulation",
                        "payee": {
                            "email": PAYEE_EMAIL
                        }
                    }
                ]
            })

        elif payment_method == "paypal":
            payment = Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [
                    {
                        "amount": {
                            "total": str(amount),
                            "currency": currency
                        },
                        "description": "Payment Simulation",
                        "payee": {
                            "email": PAYEE_EMAIL
                        }
                    }
                ],
                "redirect_urls": {
                    "return_url": "http://localhost:8001/payment/success",
                    "cancel_url": "http://localhost:8001/payment/cancel"
                }
            })

        else:
            return {"status": "ERROR", "message": "Invalid payment method. Use 'paypal' or 'credit_card'."}

 
        if payment.create():
            if payment_method == "paypal":
                for link in payment.links:
                    if link["rel"] == "approval_url":
                        return {"status": "PENDING", "approval_url": link["href"]}
            return {"status": "COMPLETED", "message": "Payment successful."}
        else:
            return {"status": "ERROR", "error": payment.error}

    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
