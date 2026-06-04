import requests
from src.config.settings import settings
from src.llm.prompts import PromptTemplates
p = PromptTemplates.INVENTORY_AGENT.format(
    query='check stock for iphone 15', 
    inventory_data='- iPhone 15 (Category: Mobiles): Price ₹79,900.00, Stock: 32 units'
)
payload = {
    "model": "sarvam-30b",
    "messages": [
        {
            "role": "user",
            "content": p
        }
    ],
    "temperature": 0.3,
    "max_tokens": 500
}
headers = {
    "Authorization": f"Bearer {settings.SARVAM_API_KEY}",
    "Content-Type": "application/json"
}
try:
    response = requests.post("https://api.sarvam.ai/v1/chat/completions", json=payload, headers=headers, timeout=60)
    import json
    with open("sarvam_debug.txt", "w", encoding="utf-8") as f:
        f.write(f"Status: {response.status_code}\nText: {response.text}")
except Exception as e:
    with open("sarvam_debug.txt", "w", encoding="utf-8") as f:
        f.write(f"Exception: {str(e)}")

