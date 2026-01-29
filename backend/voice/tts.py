import os
import uuid
from gtts import gTTS


def text_to_speech(text, lang="en"):
    """
    Converts text to speech and saves it as an MP3 file
    """

    if not text or not text.strip():
        raise ValueError("Empty text passed to TTS")

    # Create temp folder in backend root if not exists
    temp_audio_dir = os.path.join(os.path.dirname(__file__), "..", "temp_audio")
    os.makedirs(temp_audio_dir, exist_ok=True)

    # Unique filename
    filename = os.path.join(temp_audio_dir, f"{uuid.uuid4().hex}.mp3")

    # Generate speech
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    return filename
