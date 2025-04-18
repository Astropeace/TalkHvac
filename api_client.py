import requests
import json
from typing import Optional

def query_model(prompt: str, api_url: str = "http://127.0.0.1:1234", api_key: Optional[str] = None) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}" if api_key else ""
    }
    
    payload = {
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 500,
        "stop": ["\n###", "END"]
    }
    
    try:
        response = requests.post(
            f"{api_url}/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["text"]
    except Exception as e:
        return f"Error querying model: {str(e)}"
