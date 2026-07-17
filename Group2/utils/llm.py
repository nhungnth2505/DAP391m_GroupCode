import requests
import os
from config import Config

def get_llm_response(messages, system_prompt=None):
    """
    Send a conversation to the LLM and return the response.
    """
    api_key = Config.LLM_API_KEY or os.environ.get('LLM_API_KEY', '')
    endpoint = Config.LLM_API_ENDPOINT
    model = Config.LLM_MODEL

    if not api_key:
        return {
            'error': 'LLM API key not configured. Please set LLM_API_KEY environment variable.'
        }

    full_messages = []

    if system_prompt:
        full_messages.append({
            'role': 'system',
            'content': system_prompt
        })

    full_messages.extend(messages)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    payload = {
        'model': model,
        'messages': full_messages,
        'temperature': 0.7,
        'max_tokens': 300
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)

        if response.status_code == 200:
            result = response.json()
            return {
                'response': result['choices'][0]['message']['content'],
                'usage': result.get('usage', {})
            }
        else:
            return {
                'error': f'API Error: {response.status_code} - {response.text}'
            }
    except requests.exceptions.Timeout:
        return {'error': 'Request timed out. Please try again.'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Request failed: {str(e)}'}