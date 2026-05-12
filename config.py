# ============================================================
#  JARVIS CONFIG FILE
#  Put your personal settings and API keys here
# ============================================================

# ── AI PROVIDER ───────────────────────────────────────────
# Choose your free AI provider: "gemini" or "groq"
# ── AI MODEL SETTINGS ─────────────────────────────────────
# Gemini model (free tier)
GEMINI_MODEL = "gemini-1.5-flash"

# Groq model (free tier)
GROQ_MODEL = "llama3-8b-8192"

# Main model used by brain.py
AI_MODEL = GEMINI_MODEL

AI_MAX_TOKENS = 500
AI_PROVIDER = "gemini"

# Google Gemini — free at https://aistudio.google.com
GEMINI_API_KEY = "AIzaSyDIC_OsfjOI-zS0CDjnbEOPuiV7UqYgi7Y"


# ── YOUR DETAILS ──────────────────────────────────────────
USER_NAME = "Ayesha"

# ── WAKE WORD ─────────────────────────────────────────────
WAKE_WORD = "ayesha"

# ── VOICE SETTINGS ────────────────────────────────────────
VOICE_RATE = 175        # Speed of speech (words per minute)
VOICE_VOLUME = 1.0      # Volume 0.0 to 1.0
VOICE_GENDER = "male"   # "male" or "female"

# ── FACE RECOGNITION ──────────────────────────────────────
FACE_RECOGNITION_ENABLED = True
KNOWN_FACES_DIR = "data/known_faces"
FACE_RECOGNITION_TOLERANCE = 0.5

# ── AI MODEL SETTINGS ─────────────────────────────────────
# Gemini model (free tier)
GEMINI_MODEL = "gemini-1.5-flash"

# Groq model (free tier) — alternatives: "llama3-70b-8192", "mixtral-8x7b-32768"
GROQ_MODEL = "llama3-8b-8192"

AI_MAX_TOKENS = 500

AI_SYSTEM_PROMPT = f"""You are Jarvis, a smart AI assistant for {USER_NAME}.
You are helpful, concise, and slightly witty like the Jarvis from Iron Man.
Keep responses SHORT (2-3 sentences max) since they will be spoken aloud.
Do not use markdown, bullet points, or formatting — just plain spoken sentences."""

# ── APPS ──────────────────────────────────────────────────
APP_MAP = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "terminal": "cmd.exe",
}

# ── WEBSITES ──────────────────────────────────────────────
WEBSITE_MAP = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "github": "https://github.com",
    "whatsapp": "https://web.whatsapp.com",
    "gmail": "https://gmail.com",
    "chatgpt": "https://chat.openai.com",
    "netflix": "https://netflix.com",
    "twitter": "https://twitter.com",
    "instagram": "https://instagram.com",
}