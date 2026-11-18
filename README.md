<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4A0D2E,50:C2185B,100:FF8FC7&height=200&section=header&text=VoiceIQ&fontSize=58&fontColor=FFFFFF&fontAlignY=36&desc=Ask%20a%20website%20a%20question%20out%20loud%2C%20hear%20three%20AI%20models%20answer&descSize=16&descAlignY=58" width="100%" alt="VoiceIQ"/>

<p>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Deepgram-13EF93?style=for-the-badge&logoColor=black" alt="Deepgram"/>
  <img src="https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge&logo=meta&logoColor=white" alt="FAISS"/>
  <img src="https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Gemini"/>
  <img src="https://img.shields.io/badge/OpenRouter-6566F1?style=for-the-badge" alt="OpenRouter"/>
  <img src="https://img.shields.io/badge/License-MIT-FF4FA3?style=for-the-badge" alt="MIT License"/>
</p>

</div>

---

## What it does

Parents, students and visitors usually have to dig through dozens of pages to find one fact on an organisation's website. **VoiceIQ** lets them **just ask out loud**. It crawls the site into a private knowledge base, listens to the question, finds the relevant passages and has **three language models answer in parallel**, each answer read back as speech.

Every answer is grounded: the models may only use the retrieved website text, and if the answer is not there they say so instead of guessing. The demo knowledge base is built from a school website.

A recorded walkthrough is in [`Video/Sample_Video.mp4`](Video/Sample_Video.mp4).

## How a question flows

```
🎤 Browser recording
      │  POST /ask-voice (audio)
      ▼
Deepgram nova-2  ──>  question text
      │
      ▼
FAISS search over website chunks (all-MiniLM-L6-v2 embeddings, top 5)
      │
      ▼
Three LLM slots run in parallel (ThreadPoolExecutor)
  ├── Gemini (Google AI)
  ├── Kimi slot (OpenRouter)
  └── DeepSeek (OpenRouter)
      │
      ▼
gTTS turns each answer into MP3  ──>  JSON: question, three answers, three audio clips
```

## Building the knowledge base

`backend/core/ingest.py` turns any website into searchable chunks:

1. **Crawl** the site from its home page, staying on the same domain, up to depth 3.
2. **Clean** each page's HTML into plain text with BeautifulSoup.
3. **Chunk** the text into 900-character pieces with 200 characters of overlap, so no fact is cut in half.
4. **Embed** each chunk with Sentence Transformers (`all-MiniLM-L6-v2`).
5. **Save** pages, chunks and vectors to `backend/data/` as JSON.

At start-up, `rag.py` loads the vectors into a FAISS index for fast similarity search. Change `BASE_URL` in `ingest.py` and rerun it to point VoiceIQ at a different website.

## Features

- **Voice in, voice out:** speak a question, listen to the answers.
- **Three opinions at once:** compare how different models answer the same grounded question, side by side.
- **Grounded answers only:** a strict prompt forbids outside knowledge and handles greetings politely.
- **Fast:** model calls run concurrently, and audio is generated in memory and sent as hex in the JSON response.
- **Secrets kept out of code:** all API keys load from a `.env` file.

## Run it

```bash
git clone https://github.com/21Afnan/VoiceIQ.git
cd VoiceIQ
pip install -r backend/requirements.txt
```

Create `.env` in the project root:

```
DEEPGRAM_API_KEY=your_key
GEMINI_API_KEY=your_key
OPENROUTER_API_KEY=your_key       # DeepSeek slot
OPENROUTER_API_KEY2=your_key      # Kimi slot (can be the same key)
```

Build the knowledge base (optional, sample data is included) and start the API:

```bash
python -m backend.core.ingest
uvicorn backend.app:app --reload --port 8000
```

Then open `frontend/index.html`, allow the microphone and ask a question.

## API

| Method | Endpoint | Input | Returns |
|---|---|---|---|
| `GET` | `/` | | health check |
| `POST` | `/ask-voice` | audio file | question text, one answer per model, one MP3 (hex) per model |

## Project structure

```
VoiceIQ/
├── backend/
│   ├── app.py              # FastAPI app and /ask-voice
│   ├── config.py
│   ├── core/
│   │   ├── ingest.py       # crawl, clean, chunk, embed
│   │   ├── rag.py          # FAISS retriever
│   │   └── answer_engine.py# parallel multi-LLM answers
│   ├── llms/               # gemini.py, kimi.py, deepseek.py, prompts/
│   ├── voice/              # stt.py (Deepgram), tts.py (gTTS)
│   └── data/               # pages, chunks, embeddings
├── frontend/               # index.html and config.js
└── Video/                  # demo recording
```

---

<div align="center">

**Afnan Shoukat**

<a href="mailto:afnanshoukat35@gmail.com"><img src="https://img.shields.io/badge/Email-afnanshoukat35%40gmail.com-FF4FA3?style=for-the-badge&logo=gmail&logoColor=white&labelColor=4A0D2E" alt="Email"/></a>
<a href="https://www.linkedin.com/in/afnanshoukat"><img src="https://img.shields.io/badge/LinkedIn-Afnan%20Shoukat-FF4FA3?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=4A0D2E" alt="LinkedIn"/></a>
<a href="https://github.com/21Afnan"><img src="https://img.shields.io/badge/GitHub-21Afnan-FF4FA3?style=for-the-badge&logo=github&logoColor=white&labelColor=4A0D2E" alt="GitHub"/></a>

Released under the [MIT License](LICENSE).

</div>
