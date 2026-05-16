import requests
import json
import time
import configuration as config

class HuggingBrain:
    """
    A stable wrapper for Hugging Face Inference Router (OpenAI compatible).
    Provides high-reliability access to top open-source models.
    """
    def __init__(self, token=None, model="Qwen/Qwen2.5-Coder-32B-Instruct"):
        self.api_url = "https://router.huggingface.co/v1/chat/completions"
        self.token = token or config.HF_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.model = model

    def ask(self, prompt, system_prompt="You are a helpful AI assistant."):
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)
            result = response.json()
            
            if response.status_code == 200:
                return result['choices'][0]['message']['content'].strip()
            
            return f"Error: Hugging Face Router failed with {response.status_code}: {result}"
                
        except Exception as e:
            return f"Error: Hugging Face Router Exception: {str(e)}"

# Global instance
brain = HuggingBrain()
