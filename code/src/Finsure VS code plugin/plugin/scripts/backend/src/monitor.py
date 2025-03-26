import httpx
from src.config import MARBLE_API_URL

async def detect_fraud(transaction_data):
    """Send transaction data to Marble for fraud analysis."""
    url = f"{MARBLE_API_URL}/api/v1/decision"
    
    try:
        response = httpx.post(url, json=transaction_data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"Marble API Error: {e.response.text}"}
