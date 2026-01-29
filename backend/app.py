from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from backend.core.answer_engine import AnswerEngine
from backend.voice.stt import speech_to_text
from backend.voice.tts import text_to_speech
from fastapi.staticfiles import StaticFiles

# -----------------------------
# App Initialization
# -----------------------------
app = FastAPI(
    title="VoiceIQ API",
    description="Voice-only Multi-LLM RAG System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = AnswerEngine()

# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def health():
    return {"status": "ok", "message": "VoiceIQ API running"}
# -----------------------------
# VOICE → TEXT → ANSWER → VOICE
# -----------------------------
@app.post("/ask-voice")
async def ask_voice(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()

        # 1️⃣ Speech → Text
        stt_result = speech_to_text(audio_bytes)

        #  NORMALIZE STT OUTPUT
        if isinstance(stt_result, dict):
            transcript = stt_result.get("text", "")
        else:
            transcript = str(stt_result)

        transcript = transcript.strip()

        if not transcript:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

        # 2️⃣ Get AI answers (TEXT + AUDIO)
        engine_results = engine.answer(transcript)

        # 3️⃣ Extract text and convert audio files to hex
        answers_text = {}
        answers_audio = {}
        
        for model, result in engine_results.items():
            # Extract text
            text = result.get('text', '') if isinstance(result, dict) else str(result)
            answers_text[model] = text
            
            # Convert audio (bytes or filepath) to hex
            audio_value = result.get('audio') if isinstance(result, dict) else None
            if not audio_value:
                answers_audio[model] = None
                continue

            try:
                if isinstance(audio_value, (bytes, bytearray)):
                    audio_bytes = bytes(audio_value)
                elif isinstance(audio_value, str):
                    with open(audio_value, 'rb') as f:
                        audio_bytes = f.read()
                else:
                    raise TypeError(f"Unsupported audio type: {type(audio_value)}")

                answers_audio[model] = audio_bytes.hex()
                print(f"✅ Audio hex generated for {model}: {len(audio_bytes)} bytes")
            except Exception as e:
                print(f"❌ Audio hex failed for {model}: {str(e)}")
                answers_audio[model] = None

        return {
            "question_voice_text": transcript,
            "answers_text": answers_text,
            "answers_audio": answers_audio
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

