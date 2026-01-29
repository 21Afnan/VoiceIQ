/**
 * VoiceIQ Frontend Configuration
 * Handles API integration, timeouts, error handling, and audio processing
 */

// ============================================
// API CONFIGURATION
// ============================================
const API_CONFIG = {
    BASE_URL: 'http://localhost:8000',
    ENDPOINTS: {
        HEALTH: '/',
        ASK_VOICE: '/ask-voice'
    },
    TIMEOUT: 60000, // 60 seconds timeout for voice processing
    RETRY_ATTEMPTS: 3,
    RETRY_DELAY: 1000 // 1 second between retries
};

// ============================================
// ENVIRONMENT DETECTION
// ============================================
function isProduction() {
    return window.location.hostname !== 'localhost' && 
           window.location.hostname !== '127.0.0.1';
}

// ============================================
// API ERROR HANDLER
// ============================================
class APIError extends Error {
    constructor(message, status, details = '') {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.details = details;
    }
}

// ============================================
// FETCH WITH TIMEOUT
// ============================================
async function fetchWithTimeout(url, options = {}, timeout = API_CONFIG.TIMEOUT) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            let errorMessage = `HTTP ${response.status}`;
            let details = '';

            try {
                const errorData = await response.json();
                details = errorData.detail || errorData.message || '';
            } catch (e) {
                // Response is not JSON
            }

            throw new APIError(errorMessage, response.status, details);
        }

        return response;
    } catch (error) {
        clearTimeout(timeoutId);

        if (error.name === 'AbortError') {
            throw new APIError(
                'Request timeout',
                408,
                `Request took longer than ${timeout}ms. Check if backend is running.`
            );
        }

        if (error instanceof APIError) {
            throw error;
        }

        if (error instanceof TypeError) {
            throw new APIError(
                'Network error',
                0,
                'Cannot reach backend. Make sure API is running on ' + API_CONFIG.BASE_URL
            );
        }

        throw error;
    }
}

// ============================================
// RETRY LOGIC
// ============================================
async function fetchWithRetry(url, options = {}, retries = API_CONFIG.RETRY_ATTEMPTS) {
    let lastError;

    for (let attempt = 1; attempt <= retries; attempt++) {
        try {
            return await fetchWithTimeout(url, options);
        } catch (error) {
            lastError = error;
            console.warn(`Attempt ${attempt}/${retries} failed:`, error.message);

            // Don't retry on client errors (4xx) or API errors
            if (error.status >= 400 && error.status < 500) {
                throw error;
            }

            // Wait before retrying
            if (attempt < retries) {
                await new Promise(resolve => 
                    setTimeout(resolve, API_CONFIG.RETRY_DELAY * attempt)
                );
            }
        }
    }

    throw lastError;
}

// ============================================
// SEND VOICE TO API
// ============================================
async function sendVoiceToAPI(audioBlob) {
    if (!audioBlob || audioBlob.size === 0) {
        throw new APIError('Empty audio', 400, 'No audio data to send');
    }

    const formData = new FormData();
    formData.append('file', audioBlob, 'audio.wav');

    const url = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ASK_VOICE}`;

    try {
        const response = await fetchWithRetry(url, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        return data;
    } catch (error) {
        if (error instanceof APIError) {
            throw error;
        }
        throw new APIError(
            'Failed to process voice',
            500,
            error.message
        );
    }
}

// ============================================
// VALIDATE HEX STRING
// ============================================
function isValidHexString(hex) {
    if (!hex || typeof hex !== 'string') {
        return false;
    }

    // Check if string is valid hex
    if (!/^[0-9a-fA-F]*$/.test(hex)) {
        return false;
    }

    // Check if length is even
    if (hex.length % 2 !== 0) {
        return false;
    }

    // Minimum size check (at least 50 bytes for valid MP3)
    if (hex.length < 100) {
        return false;
    }

    return true;
}

// ============================================
// HEX TO BYTES CONVERSION
// ============================================
function hexToBytes(hex) {
    if (!isValidHexString(hex)) {
        throw new Error('Invalid hex string');
    }

    try {
        const bytes = new Uint8Array(
            hex.match(/.{1,2}/g).map(b => parseInt(b, 16))
        );
        return bytes;
    } catch (error) {
        throw new Error('Failed to convert hex to bytes: ' + error.message);
    }
}

// ============================================
// PLAY AUDIO FROM HEX
// ============================================
async function playAudioFromHex(hex, onError = null) {
    try {
        if (!isValidHexString(hex)) {
            throw new Error('Invalid or empty audio data');
        }

        const bytes = hexToBytes(hex);
        const blob = new Blob([bytes], { type: 'audio/mpeg' });
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);

        return new Promise((resolve, reject) => {
            audio.onplay = () => {
                console.log('Audio playback started');
            };

            audio.onended = () => {
                console.log('Audio playback ended');
                URL.revokeObjectURL(url);
                resolve();
            };

            audio.onerror = (e) => {
                console.error('Audio playback error:', e);
                URL.revokeObjectURL(url);
                const error = new Error(`Audio playback failed: ${audio.error?.message || 'Unknown error'}`);
                if (onError) onError(error);
                reject(error);
            };

            audio.play().catch(error => {
                console.error('Failed to start audio playback:', error);
                URL.revokeObjectURL(url);
                if (onError) onError(error);
                reject(error);
            });
        });
    } catch (error) {
        console.error('Error playing audio:', error);
        if (onError) onError(error);
        throw error;
    }
}

// ============================================
// STOP AUDIO PLAYBACK
// ============================================
function stopAudioPlayback() {
    const audioElements = document.querySelectorAll('audio');
    audioElements.forEach(audio => {
        audio.pause();
        audio.currentTime = 0;
    });
}

// ============================================
// CHECK API HEALTH
// ============================================
async function checkAPIHealth() {
    try {
        const url = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.HEALTH}`;
        const response = await fetchWithTimeout(url, { method: 'GET' }, 5000);
        const data = await response.json();
        return data.status === 'ok';
    } catch (error) {
        console.warn('API health check failed:', error.message);
        return false;
    }
}

// ============================================
// FORMAT ERROR MESSAGE
// ============================================
function formatErrorMessage(error) {
    if (error instanceof APIError) {
        if (error.details) {
            return `${error.message}: ${error.details}`;
        }
        return error.message;
    }

    if (error instanceof Error) {
        return error.message;
    }

    return String(error);
}

// ============================================
// RECORDING COUNTER & SAVER
// ============================================
let recordingCount = 0;

function getRecordingFileName(agentName = 'recording') {
    recordingCount++;
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
    return `${agentName}_${recordingCount}_${timestamp}.wav`;
}

function resetRecordingCounter() {
    recordingCount = 0;
}

// ============================================
// LOGGER
// ============================================
const Logger = {
    info: (msg, data = null) => {
        console.log('[VoiceIQ]', msg, data || '');
    },
    warn: (msg, data = null) => {
        console.warn('[VoiceIQ]', msg, data || '');
    },
    error: (msg, data = null) => {
        console.error('[VoiceIQ]', msg, data || '');
    },
    debug: (msg, data = null) => {
        if (!isProduction()) {
            console.debug('[VoiceIQ]', msg, data || '');
        }
    }
};

// ============================================
// EXPORT ALL
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        API_CONFIG,
        isProduction,
        APIError,
        fetchWithTimeout,
        fetchWithRetry,
        sendVoiceToAPI,
        isValidHexString,
        hexToBytes,
        playAudioFromHex,
        stopAudioPlayback,
        checkAPIHealth,
        formatErrorMessage,
        Logger
    };
}
