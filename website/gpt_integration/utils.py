# gpt_integration/utils.py
import requests
from django.conf import settings

def generate_text(prompt):
    api_key = settings.GPT3_API_KEY
    endpoint = 'https://api.openai.com/v1/engines/davinci-codex/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    data = {
        'prompt': prompt,
        'max_tokens': 2048,  # Adjust as needed
        'temperature' : 0.1
    }

    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None
