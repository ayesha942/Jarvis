# ============================================================
#  SPEAKER MODULE
#  Converts text → spoken audio using pyttsx3
#  This is called "Text-to-Speech" (TTS)
# ============================================================

import pyttsx3
import config

class Speaker:
    """
    The Speaker class wraps pyttsx3 — an OFFLINE text-to-speech library.
    'Offline' means it doesn't need the internet to speak. 
    It uses your OS's built-in voice engine:
      - Windows: SAPI5
      - Mac: NSSpeechSynthesizer
      - Linux: eSpeak
    """

    def __init__(self):
        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        self._configure_voice()

    def _configure_voice(self):
        """Set up voice properties from config."""
        
        # Set speech rate (how fast Jarvis talks)
        self.engine.setProperty('rate', config.VOICE_RATE)
        
        # Set volume (0.0 = silent, 1.0 = full volume)
        self.engine.setProperty('volume', config.VOICE_VOLUME)
        
        # Get all available voices on this system
        voices = self.engine.getProperty('voices')
        
        # Choose male or female voice
        # voices[0] is usually male, voices[1] is usually female
        # (depends on what's installed on your OS)
        if config.VOICE_GENDER == "female" and len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        else:
            self.engine.setProperty('voice', voices[0].id)

    def speak(self, text: str):
        """
        Convert text to speech and play it.
        
        How it works:
        1. pyttsx3 sends text to your OS speech engine
        2. OS converts it to audio samples
        3. Audio plays through your speakers
        4. runAndWait() blocks until speaking is done
        """
        print(f"🤖 Jarvis: {text}")  # Also print so you can read it
        self.engine.say(text)
        self.engine.runAndWait()  # This is a BLOCKING call — waits until done speaking

    def speak_async(self, text: str):
        """
        Speak without waiting (non-blocking).
        Use this if you want Jarvis to speak while doing something else.
        Note: Can cause issues if called too rapidly.
        """
        print(f"🤖 Jarvis: {text}")
        self.engine.say(text)
        self.engine.startLoop(False)
        self.engine.iterate()
        self.engine.endLoop()