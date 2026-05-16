import requests
import re
import json
import time

class ShadowBrain:
    """
    A reverse-engineered wrapper for DuckDuckGo AI Chat (Shadow API).
    Provides truly free and high-limit access to models like GPT-4o-mini and Llama 3.
    """
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/event-stream",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://duckduckgo.com/",
            "x-vqd-accept": "1",
            "Origin": "https://duckduckgo.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
        self.vqd = self._fetch_vqd()

    def _fetch_vqd(self):
        """Initializes a session and retrieves the VQD token."""
        try:
            resp = requests.get("https://duckduckgo.com/duckchat/v1/status", headers=self.headers, timeout=10)
            return resp.headers.get("x-vqd-4")
        except Exception as e:
            print(f"ShadowBrain: VQD Fetch Failed: {e}")
            return None

    def ask(self, prompt):
        """Sends a prompt to the shadow API and returns the text response."""
        if not self.vqd:
            self.vqd = self._fetch_vqd()
        
        if not self.vqd:
            return "Error: Could not initialize Shadow Brain (VQD missing)."

        url = "https://duckduckgo.com/duckchat/v1/chat"
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        # Update headers with the required token
        current_headers = self.headers.copy()
        current_headers["x-vqd-4"] = self.vqd
        current_headers["Content-Type"] = "application/json"

        try:
            response = requests.post(url, headers=current_headers, json=payload, timeout=30)
            
            # Update VQD for the next request (DuckDuckGo rotates it)
            new_vqd = response.headers.get("x-vqd-4")
            if new_vqd:
                self.vqd = new_vqd
            
            if response.status_code == 200:
                # The response is an SSE stream (Server-Sent Events)
                # We need to parse the 'data' fields and concatenate the 'message' parts
                full_text = ""
                for line in response.iter_lines():
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            data_json = json.loads(data_str)
                            full_text += data_json.get("message", "")
                        except:
                            continue
                return full_text if full_text else "Error: Shadow Brain returned empty response."
            
            return f"Error: Shadow Brain failed with status {response.status_code}"
            
        except Exception as e:
            return f"Error: Shadow Brain Exception: {str(e)}"

# Global instance for easy import
brain = ShadowBrain()
