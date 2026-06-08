import os
import requests

# Load API key from .env
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def query_huggingface(model, inputs):
    """Query Hugging Face API with a given model and input data."""
    
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    response = requests.post(API_URL, headers=headers, json={"inputs": inputs})
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to get response: {response.status_code}"}
