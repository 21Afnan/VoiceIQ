import os
import requests
from dotenv import load_dotenv

# Load env variables from project root
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(env_path)

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

if not DEEPGRAM_API_KEY:
    raise EnvironmentError("❌ DEEPGRAM_API_KEY not found in .env file")


def speech_to_text(audio_bytes, content_type: str = "audio/wav"):
    url = "https://api.deepgram.com/v1/listen"

    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": content_type or "application/octet-stream"
    }

    params = {
        "model": "nova-2",
        "language": "en"
    }

    response = requests.post(
        url,
        headers=headers,
        params=params,
        data=audio_bytes,
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Deepgram STT failed: {response.status_code} {response.text}"
        )

    result = response.json()

    try:
        return result["results"]["channels"][0]["alternatives"][0]["transcript"]
    except Exception:
        return ""
