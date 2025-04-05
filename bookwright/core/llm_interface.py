# bookwright/utils/prompt_builder.py
# bookwright/core/llm_interface.py
import requests

class OllamaClient:
    def __init__(self, model='deepseek', host='http://localhost:11434'):
        self.model = model
        self.api_url = f'{host}/api/generate'

    def generate(self, prompt, options=None):
        data = {
            'model': self.model,
            'prompt': prompt,
            'stream': False
        }
        if options:
            data['options'] = options
        response = requests.post(self.api_url, json=data, timeout=120)
        response.raise_for_status()
        return response.json().get('response', '').strip()

