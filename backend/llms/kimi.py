import os
import time
import requests
from backend.config import OPENROUTER_API_KEY2

# -------- CONFIG --------
KIMI_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-chat"
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompts", "prompt.txt")

# -------- Load Prompt --------
def load_prompt():
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


class KimiLLM:
    def __init__(self):
        if not OPENROUTER_API_KEY2:
            raise EnvironmentError("OPENROUTER_API_KEY2 not found")

        self.headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY2}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "VoiceIQ"
        }

    def generate(self, question, context):
        prompt = load_prompt().format(
            question=question,
            context=context
        )

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "Answer strictly from the given context."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 300
        }

        for attempt in range(3):
            try:
                response = requests.post(
                    KIMI_API_URL,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )

                if response.status_code == 429:
                    time.sleep(2 * (attempt + 1))
                    continue

                response.raise_for_status()
                data = response.json()
                
                # Safely extract content
                if "choices" in data and len(data["choices"]) > 0:
                    choice = data["choices"][0]
                    if "message" in choice and "content" in choice["message"]:
                        return choice["message"]["content"].strip()
                
                return f"Kimi error: Invalid response format"

            except Exception as e:
                if attempt == 2:
                    return f"Kimi error: {e}"
