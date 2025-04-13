import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def ask_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct",  # or any other
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    return result["choices"][0]["message"]["content"]
