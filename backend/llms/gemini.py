import os
import google.generativeai as genai
from backend.config import GEMINI_API_KEY

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompts", "prompt.txt")

def load_prompt():
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


# Configure Gemini once
genai.configure(api_key=GEMINI_API_KEY)


class GeminiLLM:
    def __init__(self):
        #  CONFIRMED WORKING MODEL
        self.model = genai.GenerativeModel(
            model_name="models/gemini-flash-latest"
        )

    def generate(self, question, context):
        prompt = load_prompt().format(
            question=question,
            context=context
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Gemini error: {e}"
