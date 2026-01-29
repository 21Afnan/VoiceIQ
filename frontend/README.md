# 🎨 VoiceIQ Frontend

**Modern Voice-First UI for Multi-LLM AI Assistant**

---

## 📋 Overview

A beautiful, responsive web interface for VoiceIQ that provides:
- **Voice Recording** – Browser-based microphone capture
- **Real-Time Processing** – Visual feedback during AI processing
- **Multi-Model Display** – Side-by-side LLM responses
- **Audio Playback** – Listen to AI-generated speech
- **Modern Design** – Gradient aesthetics with smooth animations

---

## 🏗️ Architecture

```
frontend/
├── index.html       # Main UI (1300+ lines)
├── config.js        # API configuration & utilities
└── README.md        # You are here
```

---

## 🚀 Quick Start

### **1. Start Backend First**
```bash
# From project root
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### **2. Serve Frontend**
```bash
# From project root
cd frontend
python -m http.server 3000
```

Frontend runs at: **http://localhost:3000**

### **3. Open in Browser**
Navigate to: **http://localhost:3000**

---

## ✨ Features

### **🎤 Voice Recording**
- Click microphone button to start recording
- Real-time visual feedback (pulse animation)
- Automatic WAV conversion
- Client-side audio validation
- Silence detection (prevents empty submissions)

### **🤖 Multi-Model Display**
Three AI model cards:
- **Google Gemini** – Advanced reasoning
- **Moonshot Kimi** – Long-context specialist
- **DeepSeek** – Deep analysis

Each card shows:
- Model name & description
- Text response
- Voice playback button
- Loading/error states

### **🔊 Audio Processing**
- **Input:** Browser microphone (MediaRecorder API)
- **Format:** WAV (mono, 16-bit)
- **Output:** MP3 playback from hex strings
- **Validation:** Duration check, RMS calculation

### **🎨 Design System**
```css
Colors:
- Background: Deep space blue (#090918)
- Primary Gradient: Pink to Purple (#f43f5e → #a855f7)
- Gemini: Pink gradient
- Kimi: Blue gradient  
- DeepSeek: Orange gradient

Animations:
- Microphone pulse (recording state)
- Star background (parallax effect)
- Card hover effects (scale + shadow)
- Smooth transitions (0.2-0.3s)
```

---

## 🔧 Configuration

### **API Settings** (`config.js`)

```javascript
const API_CONFIG = {
    BASE_URL: 'http://localhost:8000',
    ENDPOINTS: {
        HEALTH: '/',
        ASK_VOICE: '/ask-voice'
    },
    TIMEOUT: 60000,        // 60 seconds
    RETRY_ATTEMPTS: 3,
    RETRY_DELAY: 1000      // 1 second between retries
};
```

### **Customization Options**

#### **Change Backend URL**
```javascript
// In config.js, line 10
BASE_URL: 'http://your-server.com:8000'
```

#### **Adjust Timeout**
```javascript
// In config.js, line 14
TIMEOUT: 90000  // 90 seconds
```

#### **Modify Audio Settings**
```javascript
// In index.html (JavaScript section)
const MIN_AUDIO_SECONDS = 0.35;      // Minimum recording length
const SILENCE_RMS_THRESHOLD = 0.008; // Silence detection sensitivity
const MIN_BLOB_BYTES = 1500;         // Minimum audio file size
```

---

## 📡 API Integration

### **Request Flow**
```
1. User clicks microphone → Start recording
2. User clicks again → Stop recording
3. Convert to WAV → Validate audio
4. POST /ask-voice → Send to backend
5. Receive JSON → Display responses
6. Decode hex audio → Play MP3
```

### **Request Format**
```javascript
POST http://localhost:8000/ask-voice
Content-Type: multipart/form-data

Body:
  file: audio.wav (binary)
```

### **Response Format**
```json
{
  "question_voice_text": "User's transcribed question",
  "answers_text": {
    "Gemini": "Text response from Gemini",
    "DeepSeek": "Text response from DeepSeek",
    "Kimi": "Text response from Kimi"
  },
  "answers_audio": {
    "Gemini": "48656c6c6f...",  // Hex-encoded MP3
    "DeepSeek": "48656c6c6f...",
    "Kimi": "48656c6c6f..."
  }
}
```

---

## 🎯 User Interaction Flow

### **1. Initial State (Idle)**
```
┌─────────────────────────────┐
│   Click microphone icon     │
│   "Click to start speaking" │
└─────────────────────────────┘
```

### **2. Recording State**
```
┌─────────────────────────────┐
│   🔴 Recording...            │
│   Pulse animation active     │
│   "Click to stop"            │
└─────────────────────────────┘
```

### **3. Processing State**
```
┌─────────────────────────────┐
│   Converting audio...        │
│   Uploading...               │
│   Waiting for AI...          │
└─────────────────────────────┘
```

### **4. Results State**
```
┌─────────────────────────────┐
│   Transcribed question       │
│   ┌─────────────────────┐   │
│   │  Gemini Response     │   │
│   │  [Play Voice] 🔊     │   │
│   └─────────────────────┘   │
│   ┌─────────────────────┐   │
│   │  DeepSeek Response   │   │
│   └─────────────────────┘   │
│   ┌─────────────────────┐   │
│   │  Kimi Response       │   │
│   └─────────────────────┘   │
└─────────────────────────────┘
```

---

## 🛠️ Technical Details

### **Audio Processing**

#### **Recording**
```javascript
MediaRecorder API (WebRTC)
↓
Supported formats:
1. audio/webm;codecs=opus (preferred)
2. audio/webm (fallback)
3. audio/mp4 (Safari fallback)
```

#### **Conversion to WAV**
```javascript
AudioContext API
↓
1. Decode audio buffer
2. Downmix to mono
3. Calculate RMS (silence detection)
4. Encode to WAV (16-bit PCM)
```

#### **Playback**
```javascript
Hex string → Uint8Array → Blob → Object URL
↓
<audio> element playback
```

### **Error Handling**

```javascript
// Retry Logic
Attempt 1 → Fail → Wait 1s
Attempt 2 → Fail → Wait 2s
Attempt 3 → Fail → Show error

// Error Types
- Network errors (fetch failures)
- Timeout errors (60s exceeded)
- Audio errors (empty, silent)
- Backend errors (HTTP 4xx/5xx)
```

### **State Management**
```javascript
// Global State Variables
isRecording: boolean      // Mic active?
isBusy: boolean          // Processing request?
mediaRecorder: MediaRecorder
audioChunks: Blob[]

// State Transitions
idle → recording → processing → displaying → idle
```

---

## 🎨 UI Components

### **Header**
```html
- Logo icon with gradient
- App name "VoiceIQ"
- Powered by badges (Gemini, Kimi, DeepSeek)
```

### **Microphone Section**
```html
- Title & instructions
- Large circular mic button
- Pulse animation (recording state)
- Status text (below button)
- Error message box (hidden by default)
```

### **Features Section** (Idle state)
```html
- Feature badges
  • Fast & Accurate
  • Multi-Model
  • Voice Enabled
```

### **Results Section** (Active state)
```html
- Transcribed question box
- Three model cards (Gemini, Kimi, DeepSeek)
  • Model icon
  • Model name & description
  • Text response
  • Voice playback button
```

### **Star Background**
```javascript
100 animated stars
- Random positions
- Random sizes (1-3px)
- Twinkle animation (3s)
- Fixed positioning
```

---

## 📱 Responsive Design

### **Desktop (>768px)**
```css
- Full header with badges
- Large mic button (180px)
- 3-column grid for model cards
- Centered layout (max-width: 1400px)
```

### **Mobile (<768px)**
```css
- Stacked header
- Smaller mic button (150px)
- Single column for cards
- Touch-optimized buttons
```

---

## 🚀 Deployment

### **Static Hosting**
Deploy `index.html` and `config.js` to:
- **Vercel** – `vercel deploy`
- **Netlify** – Drag & drop
- **GitHub Pages** – Push to `gh-pages` branch
- **AWS S3** – Static website hosting

### **Update Backend URL**
```javascript
// config.js
BASE_URL: 'https://your-api.com'
```

### **CORS Configuration**
Ensure backend allows your domain:
```python
# backend/app.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 Troubleshooting

### **Microphone Access Denied**
```
Error: "Microphone access denied or unavailable"
Solution: Grant browser microphone permissions
Chrome: Settings → Privacy → Microphone
```

### **Cannot Connect to Backend**
```
Error: "Cannot connect to backend at http://localhost:8000"
Solution: 
1. Start backend server
2. Check CORS configuration
3. Verify API_CONFIG.BASE_URL in config.js
```

### **Audio Not Playing**
```
Issue: Voice button disabled or audio doesn't play
Solution:
1. Check browser console for errors
2. Verify audio hex data is valid
3. Test with different browser
```

### **Empty Audio Error**
```
Error: "Audio empty (no speech detected)"
Solution:
1. Speak louder and closer to mic
2. Check microphone input levels
3. Try recording longer (>0.5 seconds)
```

---

## 🎯 Browser Compatibility

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 80+ | ✅ Full |
| Firefox | 75+ | ✅ Full |
| Safari | 14+ | ✅ Full |
| Edge | 80+ | ✅ Full |
| Opera | 67+ | ✅ Full |

**Required APIs:**
- MediaRecorder API
- Web Audio API
- Fetch API
- Promises/Async

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| **Page Load** | ~1-2 seconds |
| **Recording Start** | Instant |
| **Audio Conversion** | ~500ms |
| **Upload Time** | ~1-2 seconds |
| **UI Responsiveness** | 60 FPS |
| **Bundle Size** | ~150KB (inline) |

---

## 🔐 Security Considerations

- ✅ HTTPS required for microphone access (production)
- ✅ No sensitive data stored in localStorage
- ✅ Audio files not persisted client-side
- ✅ CORS enforced by backend
- ✅ No external script dependencies (self-contained)

---

## 🎨 Customization Guide

### **Change Colors**
```css
/* In index.html <style> section */
:root {
    --bg-dark: #090918;                    /* Background color */
    --primary-gradient: linear-gradient(135deg, #f43f5e, #a855f7);
    --gemini-gradient: linear-gradient(135deg, #f093fb, #f5576c);
    --kimi-gradient: linear-gradient(135deg, #4facfe, #00f2fe);
    --deepseek-gradient: linear-gradient(135deg, #fa709a, #fee140);
}
```

### **Add New Model**
```html
<!-- Duplicate this structure in index.html -->
<div class="card your-model">
    <div class="card-header">
        <div class="model-icon your-model-icon">
            <i class="fa-solid fa-your-icon"></i>
        </div>
        <div class="model-info">
            <h3 class="your-model-text">Your Model Name</h3>
            <span>Description</span>
        </div>
    </div>
    <div class="error-box-card">
        <div class="error-title">Waiting</div>
        <div class="error-desc">Ask a question to see response.</div>
    </div>
</div>
```

---

## 📝 License

MIT License - See root LICENSE file

---

## 🔗 Related Documentation

- [Main README](../README.md)
- [Backend README](../backend/README.md)

---

**Designed with ❤️ for modern voice-first AI experiences**
