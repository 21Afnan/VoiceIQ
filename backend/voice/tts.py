import os
import uuid
from io import BytesIO
from gtts import gTTS


def text_to_speech(text, lang="en", return_bytes: bool = True):
    """
    Converts text to speech.

    By default returns MP3 bytes in-memory (avoids filesystem writes).
    Set return_bytes=False to save to a temp MP3 file and return its path.
    """

    if not text or not text.strip():
        raise ValueError("Empty text passed to TTS")

    # Generate speech
    tts = gTTS(text=text, lang=lang)

    if return_bytes:
        buf = BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()

    # Fallback: write to filesystem
    temp_audio_dir = os.path.join(os.path.dirname(__file__), "..", "temp_audio")
    os.makedirs(temp_audio_dir, exist_ok=True)
    filename = os.path.join(temp_audio_dir, f"{uuid.uuid4().hex}.mp3")
    tts.save(filename)
    return filename
