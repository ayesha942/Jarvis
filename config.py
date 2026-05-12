# ============================================================
#  JARVIS CONFIG FILE
#  Put your personal settings and API keys here
# ============================================================

# Your Anthropic API Key — get it from https://console.anthropic.com
ANTHROPIC_API_KEY = "your_anthropic_api_key_here"

# Your name — Jarvis will greet you by this
USER_NAME = "Boss"

# Wake word — what you say to wake Jarvis up
WAKE_WORD = "jarvis"

# Voice settings for text-to-speech
VOICE_RATE = 175        # Speed of speech (words per minute)
VOICE_VOLUME = 1.0      # Volume 0.0 to 1.0
VOICE_GENDER = "male"   # "male" or "female"

# Face recognition settings
FACE_RECOGNITION_ENABLED = True
KNOWN_FACES_DIR = "data/known_faces"
FACE_RECOGNITION_TOLERANCE = 0.5  # Lower = stricter (0.4-0.6 is good)

# AI Model settings
AI_MODEL = "claude-sonnet-4-20250514"
AI_MAX_TOKENS = 500
AI_SYSTEM_PROMPT = f"""You are Jarvis, a smart AI assistant for {USER_NAME}.
You are helpful, concise, and slightly witty like the Jarvis from Iron Man.
Keep responses SHORT (2-3 sentences max) since they will be spoken aloud.
Do not use markdown, bullet points, or formatting — just plain spoken sentences."""

# Apps to open by voice command (command word: app path or URL)
APP_MAP = {
    "notepad": "notepad.exe",           # Windows
    "calculator": "calc.exe",           # Windows
    "paint": "mspaint.exe",             # Windows
    "terminal": "cmd.exe",              # Windows
    # For Mac, use: "calculator": "open -a Calculator"
    # For Linux, use: "calculator": "gnome-calculator"
}

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