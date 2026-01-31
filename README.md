<div align="center">

# 🎙️ VoiceIQ  
### **Voice-First Multi-Model AI Assistant**  

<p align="center">
  <strong><em>Talk to AI. Hear from many minds. One intelligent voice.</em></strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Production Ready-success?style=flat-square&color=10B981"/>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi"/>
  <img src="https://img.shields.io/badge/Multi--LLM-Orchestration-FF6B6B?style=flat-square"/>
  <img src="https://img.shields.io/badge/Voice--AI-STT%20%7C%20TTS-E91E63?style=flat-square"/>
</p>

<p align="center">
  <strong>
    Voice-First AI • RAG-Powered • Multi-LLM • Production-Ready
  </strong>
</p>

</div>

---

## 🌟 About VoiceIQ

**VoiceIQ** is a production-ready voice-first AI system that demonstrates modern best practices in AI application development:

- 🎤 **Voice-Native Interaction** – Speak naturally and hear AI respond  
- 🧠 **Multi-Model Intelligence** – Get answers from 3 different AI models simultaneously  
- 📚 **Knowledge-Aware (RAG)** – AI understands domain-specific context via semantic search  
- ⚡ **Parallel Processing** – Fast, concurrent LLM inference  
- 🎨 **Beautiful UI** – Modern, responsive frontend with gradient design  
- 🏗️ **Clean Architecture** – Scalable, maintainable, production-grade codebase  

> Perfect for portfolios, demos, startups, and AI research prototypes.

---

## ✨ Key Features

| Feature | Details |
|---------|---------|
| 🎤 **Live Voice Recording** | Intuitive microphone-based interaction |
| 🎧 **Speech-to-Text** | Powered by Deepgram API (neural accuracy) |
| 🧠 **Intelligent Retrieval** | FAISS-based semantic search with sentence embeddings |
| 🤖 **Triple LLM Power** | Google Gemini • DeepSeek • Moonshot Kimi |
| ⚙️ **Parallel Orchestration** | Concurrent inference (3 models simultaneously) |
| 🔊 **Natural Speech Output** | Google Text-to-Speech with audio playback |
| 🎨 **Responsive Design** | Mobile-friendly UI with gradient aesthetics |
| 🔐 **Secure** | Environment-based secret management |
| 📊 **Production-Grade** | Error handling, timeouts, retry logic |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                         │
│                  (Browser / Frontend)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓ (Audio File)
┌─────────────────────────────────────────────────────────────┐
│                  FRONTEND (Port 3000)                        │
│            Microphone Recording • Audio Processing           │
│         Vue/React-like UI with Gradient Design              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓ (POST /ask-voice)
┌─────────────────────────────────────────────────────────────┐
│                 FASTAPI BACKEND (Port 8000)                 │
│              Async Request Handling • CORS Setup            │
└──────────────────────┬──────────────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │  STT     │ │   RAG    │ │   LLMs   │
    │(Deepgram)│ │  (FAISS) │ │(Parallel)│
    └──────────┘ └──────────┘ └──────────┘
          │            │            │
          └────────────┼────────────┘
                       ↓
            ┌─────────────────────┐
            │   TTS + Audio Hex   │
            │   (Google gTTS)     │
            └──────────┬──────────┘
                       │
                       ↓ (JSON Response)
         ┌──────────────────────────────┐
         │ Question + Answers + Audio   │
         └──────────────────────────────┘
```

---

## 📂 Project Structure

```
VoiceIQ/
├── 📄 README.md                 # You are here
├── 🔑 .env                      # API keys (KEEP SECRET!)
├── 📋 requirements.txt          # Python dependencies
├── .gitignore                   # Git ignore rules
│
├── backend/                     # ⚡ FastAPI Backend
│   ├── app.py                   # Main FastAPI application
│   ├── config.py                # Configuration & API keys
│   │
│   ├── core/                    # Core AI Logic
│   │   ├── answer_engine.py     # LLM orchestrator (parallel inference)
│   │   ├── rag.py               # RAG retriever (FAISS + embeddings)
│   │   └── ingest.py            # Data ingestion pipeline
│   │
│   ├── llms/                    # LLM Integrations
│   │   ├── gemini.py            # Google Gemini API
│   │   ├── deepseek.py          # DeepSeek (via OpenRouter)
│   │   ├── kimi.py              # Kimi (via OpenRouter)
│   │   └── prompts/
│   │       └── prompt.txt       # System prompt template
│   │
│   ├── voice/                   # Voice Processing
│   │   ├── stt.py               # Speech-to-Text (Deepgram)
│   │   └── tts.py               # Text-to-Speech (Google gTTS)
│   │
│   ├── data/                    # Knowledge Base (RAG)
│   │   ├── chunks.json          # Vectorized text chunks
│   │   ├── embeddings.json      # Vector embeddings
│   │   └── pages.json           # Source metadata
│   │
│   ├── temp_audio/              # Runtime TTS output (auto-created)
│   └── tests/                   # Validation & integration tests
│
└── frontend/                    # 🎨 Web UI
    ├── index.html               # Main page (1300+ lines)
    └── config.js                # API config & utilities
```

---

## ⚙️ Technology Stack

### **Backend**
```
FastAPI (0.110.0)              Modern async Python web framework
Uvicorn                         ASGI server for FastAPI
Python 3.10+                    Core language
```

### **AI & Voice**
```
Google Gemini API               Latest generative AI model
OpenRouter                      Gateway for DeepSeek & Kimi
Deepgram (Nova-2)               Neural speech-to-text
Google Text-to-Speech (gTTS)    Voice synthesis
```

### **Vector Search & Embeddings**
```
FAISS (1.8.0+)                  Efficient similarity search
Sentence Transformers           Semantic embeddings (all-MiniLM-L6-v2)
NumPy                           Numerical computations
scikit-learn                    Additional ML utilities
```

### **Frontend**
```
HTML5                           Structure
CSS3 (Gradients)                Modern styling
JavaScript (Vanilla)            Client-side logic
Web Audio API                   Microphone access
Fetch API                       HTTP requests
```

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.10 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### **Step 1: Clone Repository**
```bash
git clone https://github.com/your-username/voiceiq.git
cd voiceiq
```

### **Step 2: Create Virtual Environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r backend/requirements.txt
```

### **Step 4: Configure API Keys**
```bash
# Edit .env file and add your API keys:
GEMINI_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here
OPENROUTER_API_KEY2=your_key_here
DEEPGRAM_API_KEY=your_key_here
```

### **Step 5: Start Backend**
```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Backend runs at: **http://localhost:8000**

### **Step 6: Start Frontend (New Terminal)**
```bash
cd frontend
python -m http.server 3000
```

Frontend runs at: **http://localhost:3000**

### **Step 7: Open in Browser**
Navigate to **http://localhost:3000** and start speaking! 🎤

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

### **Process Voice**
```http
POST /ask-voice
Content-Type: multipart/form-data

Body: 
  file: <audio.wav>
```

**Response:**
```json
{
  "question_voice_text": "What curriculum does Sunmarke offer?",
  "answers_text": {
    "Gemini": "Sunmarke offers the British curriculum...",
    "DeepSeek": "The school provides multiple curriculum paths...",
    "Kimi": "Sunmarke School offers A-Level, IB, and BTEC..."
  },
  "answers_audio": {
    "Gemini": "48656c6c6f...",
    "DeepSeek": "48656c6c6f...",
    "Kimi": "48656c6c6f..."
  }
}
```

---

## 🎯 Usage Guide

### **Recording & Processing**
1. **Click the microphone button** – Starts recording
2. **Speak your question** – Ask anything about the knowledge base
3. **Click again to stop** – Ends recording and sends to backend
4. **Wait for responses** – All 3 models respond in parallel (~5-10 seconds)
5. **Click voice icon** – Hear each AI's answer read aloud

### **Example Questions**
- "What curriculum does Sunmarke offer?"
- "What are the school timings?"
- "What is the tuition fee?"
- "What extracurricular activities are available?"

---

## 🧠 How It Works

### **1. Speech-to-Text (STT)**
- Deepgram API transcribes your audio to text
- Neural model provides ~95%+ accuracy
- Supports multiple languages

### **2. Retrieval-Augmented Generation (RAG)**
- Converts your question to embeddings
- Searches FAISS index for similar content
- Retrieves top 5 relevant chunks from knowledge base
- Combines chunks into context for LLMs

### **3. Parallel LLM Inference**
- Question + Context sent to all 3 models simultaneously
- Uses Python's `ThreadPoolExecutor` for concurrency
- Models run in parallel (not sequential)
- Faster response time than waiting for each model

### **4. Text-to-Speech (TTS)**
- Google gTTS converts each AI response to MP3
- MP3 converted to hex string for JSON response
- Frontend decodes hex and plays audio

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **STT Latency** | ~2-3 seconds (Deepgram) |
| **RAG Retrieval** | ~100ms (FAISS) |
| **LLM Response** | ~3-8 seconds (parallel) |
| **TTS Generation** | ~2-3 seconds per answer |
| **Total E2E** | ~10-15 seconds |
| **Concurrent Requests** | 3+ models in parallel |
| **Audio Format** | MP3 (hex-encoded in JSON) |

---

## 🔐 Security & Environment

### **Required API Keys**
Create a `.env` file in the root directory:

```env
# Google Cloud
GEMINI_API_KEY=AIzaSy...

# OpenRouter (for DeepSeek & Kimi)
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_API_KEY2=sk-or-v1-...

# Deepgram
DEEPGRAM_API_KEY=4ade...
```

### **Best Practices**
- ✅ Never commit `.env` to version control
- ✅ Use `.gitignore` to exclude secrets
- ✅ Rotate API keys regularly
- ✅ Use service accounts for production
- ✅ Monitor API usage and costs

---

---

## ⚠️ Limitations & Considerations

### **Current Limitations**
- STT requires **clear English speech**
- No audio file upload (must record in-app)
- Knowledge base is static (no real-time updates)
- Kimi availability depends on OpenRouter API status
- No user authentication (add for production)
- Single-threaded at API level (scale horizontally)

### **Future Enhancements**
- [ ] Custom knowledge base ingestion
- [ ] User authentication & API keys
- [ ] Conversation history & memory
- [ ] Custom LLM fine-tuning
- [ ] Real-time knowledge updates
- [ ] Advanced audio processing
- [ ] Multi-language support
- [ ] Deployment templates

---

## 🤝 Contributing

This is a portfolio/demo project, but contributions are welcome!

### **Ways to Contribute**
- Report bugs and issues
- Suggest new features
- Improve documentation
- Optimize performance
- Add more LLM integrations
- Enhance UI/UX

---

## 📄 License

This project is open source under the **MIT License**.

---

## 🙏 Acknowledgments

- **FastAPI** – Modern Python web framework
- **Deepgram** – Neural speech-to-text
- **Google Cloud** – Gemini & Text-to-Speech APIs
- **OpenRouter** – LLM gateway service
- **FAISS** – Vector similarity search
- **Sentence Transformers** – Embedding models

---

<div align="center">

### **Built with ❤️ for the AI community**

**VoiceIQ** demonstrates production-grade AI system design patterns.  
Perfect for learning, portfolios, and real-world applications.

**Version:** 1.0.0 | **Last Updated:** January 2026

</div>
