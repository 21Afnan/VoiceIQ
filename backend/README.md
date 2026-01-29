# 🔧 VoiceIQ Backend

**FastAPI Backend Service for Voice-First Multi-LLM AI System**

---

## 📋 Overview

This is the backend service for VoiceIQ, providing:
- **Voice Processing** – Speech-to-Text and Text-to-Speech
- **RAG System** – FAISS-based semantic search
- **Multi-LLM Orchestration** – Parallel inference from 3 AI models
- **RESTful API** – FastAPI endpoints for frontend integration

---

## 🏗️ Architecture

```
backend/
├── app.py                    # FastAPI application & routes
├── config.py                 # Configuration & API keys
├── requirements.txt          # Python dependencies
│
├── core/                     # Core AI Logic
│   ├── answer_engine.py      # LLM orchestration engine
│   ├── rag.py                # RAG retriever (FAISS)
│   └── ingest.py             # Data ingestion pipeline
│
├── llms/                     # LLM Integrations
│   ├── gemini.py             # Google Gemini API
│   ├── deepseek.py           # DeepSeek via OpenRouter
│   ├── kimi.py               # Kimi via OpenRouter
│   └── prompts/
│       └── prompt.txt        # System prompt template
│
├── voice/                    # Voice Processing
│   ├── stt.py                # Speech-to-Text (Deepgram)
│   └── tts.py                # Text-to-Speech (gTTS)
│
├── data/                     # Knowledge Base
│   ├── chunks.json           # Text chunks (~2500)
│   ├── embeddings.json       # Vector embeddings
│   └── pages.json            # Source metadata
│
└── temp_audio/               # Runtime TTS output
```

---

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Configure Environment**
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_API_KEY2=your_second_openrouter_key
DEEPGRAM_API_KEY=your_deepgram_key
```

### **3. Start Server**
```bash
# From project root
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload

# Or from backend directory
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Server runs at: **http://localhost:8000**

---

## 📡 API Endpoints

### **Health Check**
```http
GET /
```
**Response:**
```json
{
  "status": "ok",
  "message": "VoiceIQ API running"
}
```

### **Process Voice Question**
```http
POST /ask-voice
Content-Type: multipart/form-data

Body:
  file: <audio.wav>  (Audio file)
```

**Response:**
```json
{
  "question_voice_text": "What curriculum does Sunmarke offer?",
  "answers_text": {
    "Gemini": "Sunmarke offers the British curriculum...",
    "DeepSeek": "The school provides A-Level, BTEC...",
    "Kimi": "Sunmarke School offers IB Diploma..."
  },
  "answers_audio": {
    "Gemini": "48656c6c6f20576f726c64",
    "DeepSeek": "48656c6c6f20576f726c64",
    "Kimi": "48656c6c6f20576f726c64"
  }
}
```

---

## 🔧 Core Components

### **1. Answer Engine** (`core/answer_engine.py`)
Orchestrates the entire AI pipeline:
- Retrieves relevant context via RAG
- Sends queries to 3 LLMs in parallel
- Generates voice output for each response
- Returns structured JSON with text + audio

**Key Features:**
- `ThreadPoolExecutor` for parallel LLM calls
- Error handling per model
- TTS generation for all responses

### **2. RAG System** (`core/rag.py`)
Semantic search over knowledge base:
- **Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Index:** FAISS (IndexFlatL2)
- **Retrieval:** Top-K similar chunks (default: 5)

**Process:**
1. Encode query to embeddings
2. Search FAISS index
3. Return relevant text chunks
4. Combine into context for LLMs

### **3. LLM Integrations** (`llms/`)
Three production-ready LLM adapters:

**Gemini** (`gemini.py`)
```python
- Model: gemini-flash-latest
- API: Google Generative AI
- Features: Fast, accurate, multimodal
```

**DeepSeek** (`deepseek.py`)
```python
- Model: deepseek/deepseek-chat
- API: OpenRouter
- Features: Deep reasoning, structured output
```

**Kimi** (`kimi.py`)
```python
- Model: moonshot-kimi (via OpenRouter)
- API: OpenRouter (OPENROUTER_API_KEY2)
- Features: Long-context understanding
```

### **4. Voice Processing** (`voice/`)

**STT** (`stt.py`)
- **Provider:** Deepgram API
- **Model:** nova-2
- **Input:** Audio bytes (WAV)
- **Output:** Transcribed text

**TTS** (`tts.py`)
- **Provider:** Google Text-to-Speech (gTTS)
- **Input:** Text string
- **Output:** MP3 file (saved to `temp_audio/`)

---

## ⚙️ Configuration

### **Environment Variables** (`.env`)
```env
# Google Cloud
GEMINI_API_KEY=AIzaSy...

# OpenRouter
OPENROUTER_API_KEY=sk-or-v1-...      # For DeepSeek
OPENROUTER_API_KEY2=sk-or-v1-...     # For Kimi

# Deepgram
DEEPGRAM_API_KEY=4ade...
```

### **Config File** (`config.py`)
```python
# Validates all required API keys
# Raises EnvironmentError if any missing
validate_env()
```

---

## 📦 Dependencies

### **Core Framework**
- `fastapi==0.110.0` – Web framework
- `uvicorn[standard]` – ASGI server
- `python-multipart` – File upload handling

### **AI & ML**
- `google-generativeai==0.3.2` – Gemini API
- `sentence-transformers==2.6.1` – Embeddings
- `faiss-cpu>=1.8.0` – Vector search
- `numpy>=2.0.0` – Numerical computing
- `scikit-learn==1.4.0` – ML utilities

### **Voice Processing**
- `deepgram-sdk>=3.0.0` – Speech-to-Text
- `gtts>=2.5.0` – Text-to-Speech

### **Utilities**
- `requests==2.31.0` – HTTP client
- `python-dotenv==1.0.1` – Environment management
- `beautifulsoup4==4.12.3` – Web scraping (for data ingestion)

---

## 🧪 Testing

Run validation tests:
```bash
# Test RAG retrieval
python -m backend.core.rag

# Test individual LLM
python -m backend.llms.gemini

# Test voice pipeline
python -m backend.voice.stt
python -m backend.voice.tts
```

---

## 🔒 Security Best Practices

- ✅ Store API keys in `.env` (never commit)
- ✅ Use `.gitignore` to exclude secrets
- ✅ Validate all API keys on startup
- ✅ Enable CORS only for trusted origins (production)
- ✅ Add rate limiting for production
- ✅ Monitor API usage and costs

---

## 🚀 Production Deployment

### **Environment Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY=...
export OPENROUTER_API_KEY=...
export DEEPGRAM_API_KEY=...
```

### **Run with Gunicorn**
```bash
gunicorn backend.app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### **Docker Deployment**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| **Startup Time** | ~3-5 seconds |
| **RAG Retrieval** | ~100ms |
| **LLM Inference** | ~3-8 seconds (parallel) |
| **TTS Generation** | ~2-3 seconds per response |
| **Total Latency** | ~10-15 seconds |
| **Concurrent Models** | 3 (Gemini, DeepSeek, Kimi) |

---

## 🐛 Troubleshooting

### **Import Errors**
```bash
# Run from project root, not backend/
uvicorn backend.app:app --reload
```

### **Missing API Keys**
```
EnvironmentError: Missing environment variables: GEMINI_API_KEY
```
**Fix:** Add key to `.env` file

### **FAISS Errors**
```bash
# Install FAISS CPU version
pip install faiss-cpu>=1.8.0
```

### **Audio File Not Found**
- Ensure `temp_audio/` folder exists
- Check file permissions

---

## 📝 License

MIT License - See root LICENSE file

---

## 🔗 Related Documentation

- [Main README](../README.md)
- [Frontend README](../frontend/README.md)
- [API Documentation](../docs/api.md) (if exists)

---

**Built with ❤️ using FastAPI and modern AI tools**
