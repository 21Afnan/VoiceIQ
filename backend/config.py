import os
from dotenv import load_dotenv

# Load environment variables once
load_dotenv()

# -------- API KEYS --------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
KIMI_API_KEY = os.getenv("KIMI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
OPENROUTER_API_KEY2 = os.getenv("OPENROUTER_API_KEY2")
# -------- PATHS --------
PROMPT_PATH = "prompts/prompt.txt"
DATA_DIR = "data"

# -------- VALIDATION --------
def validate_env():
    missing = []
    if not GEMINI_API_KEY:
        missing.append("GEMINI_API_KEY")
    if not DEEPSEEK_API_KEY:
        missing.append("DEEPSEEK_API_KEY")
    if not KIMI_API_KEY:
        missing.append("KIMI_API_KEY")
    if not OPENROUTER_API_KEY:
        missing.append("OPENROUTER_API_KEY")    
    if not DEEPGRAM_API_KEY:
        missing.append("DEEPGRAM_API_KEY")
    if not OPENROUTER_API_KEY2:
        missing.append("OPENROUTER_API_KEY2")
    if missing:
        raise EnvironmentError(
            f"Missing environment variables: {', '.join(missing)}"
        )
