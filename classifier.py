import re
from typing import Dict, Optional
from .api_client import query_model

HVAC_CATEGORIES = [
    "Electrical", "Compressor", "Refrigerant", "Thermostat",
    "Airflow", "Sensor", "Control Board", "Condenser", 
    "Evaporator", "Other"
]

CLASSIFY_PROMPT = """<|system|>
Classify this HVAC problem description into one of these categories: {categories}
Respond only with the category name, nothing else.
</system|>
<|user|>
Problem: {problem_text}
</user|>
<|assistant|>
Category:"""

def classify_post(text: str, api_url: str) -> Dict[str, str]:
    """Classify HVAC post using LLM with regex fallback"""
    # Try LLM classification first
    llm_category = _llm_classify(text, api_url)
    if llm_category in HVAC_CATEGORIES:
        return {"category": llm_category, "source": "llm"}
        
    # Fallback to regex patterns
    regex_category = _regex_classify(text)
    return {"category": regex_category, "source": "regex"}

def _llm_classify(text: str, api_url: str) -> Optional[str]:
    prompt = CLASSIFY_PROMPT.format(
        categories=", ".join(HVAC_CATEGORIES),
        problem_text=text[:1000]  # Truncate to fit context
    )
    
    response = query_model(prompt, api_url).strip()
    return response if response in HVAC_CATEGORIES else None

def _regex_classify(text: str) -> str:
    text = text.lower()
    patterns = {
        "Electrical": r"breaker|voltage|wiring|short circuit",
        "Compressor": r"compressor|amp draw|windings",
        "Refrigerant": r"charge|refrigerant|superheat|subcool",
        "Thermostat": r"thermostat|temperature setting|programming"
    }
    
    for category, pattern in patterns.items():
        if re.search(pattern, text):
            return category
            
    return "Other"
