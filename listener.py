# ============================================================
#  LISTENER MODULE
#  Two jobs:
#   1. Detect the wake word "Jarvis" (always listening)
#   2. Capture and transcribe your voice command
# ============================================================

import speech_recognition as sr
import config

class Listener:
    """
    Uses the SpeechRecognition library which connects to Google's
    free Speech-to-Text API over the internet.
    
    Flow:
    [Microphone] → [Audio Data] → [Google API] → [Text String]
    
    Alternative APIs supported by this library:
    - Google (default, free, needs internet)
    - Sphinx (offline but less accurate)
    - Whisper (OpenAI, very accurate, runs locally)
    - Azure, AWS, IBM (paid, enterprise)
    """

    def __init__(self):
        # Create the recognizer object — this handles all audio processing
        self.recognizer = sr.Recognizer()
        
        # sr.Microphone() grabs your default system microphone
        self.microphone = sr.Microphone()
        
        # Calibrate for background noise (run once at startup)
        self._calibrate()

    def _calibrate(self):
        """
        Adjust for ambient noise in your environment.
        This sets the 'energy threshold' — the minimum loudness
        that counts as actual speech vs background noise.
        
        CONCEPT: Energy Threshold
        - Too low → picks up fan noise, AC, etc. as speech
        - Too high → misses quiet speech
        - adjust_for_ambient_noise() auto-calibrates this for 1 second
        """
        print("🎙️ Calibrating microphone for background noise...")
        with self.microphone as source:
            # Listen for 1 second of silence to calibrate
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"✅ Calibrated. Energy threshold: {self.recognizer.energy_threshold:.0f}")

    def listen_for_wake_word(self) -> bool:
        """
        Listens continuously until it hears the wake word.
        Returns True when wake word is detected.
        
        CONCEPT: Wake Word Detection
        We're doing a SIMPLE version here — listen, transcribe, check if 
        "jarvis" is in the text. 
        
        Production systems (like Alexa, Siri) use a tiny on-device neural 
        network that runs 24/7 with very low CPU usage. Libraries like 
        Porcupine (by Picovoice) do this in Python too.
        """
        print(f"\n😴 Sleeping... Say '{config.WAKE_WORD.capitalize()}' to wake me up")
        
        while True:
            try:
                audio = self._capture_audio(timeout=None, phrase_limit=3)
                if audio is None:
                    continue
                    
                text = self._transcribe(audio)
                
                if text and config.WAKE_WORD.lower() in text.lower():
                    print(f"⚡ Wake word detected!")
                    return True
                    
            except KeyboardInterrupt:
                raise  # Let main.py handle Ctrl+C
            except Exception:
                continue  # Keep listening on any error

    def listen_for_command(self) -> str:
        """
        After wake word is detected, listen for the actual command.
        Returns the transcribed command as a string.
        
        CONCEPT: Speech Recognition Pipeline
        1. Capture audio → numpy array of sound samples
        2. Convert samples → WAV format bytes
        3. Send WAV bytes → Google Speech API via HTTPS
        4. Google returns → JSON with transcribed text
        5. We return → just the text string
        """
        print("🎙️ Listening for command...")
        
        audio = self._capture_audio(timeout=5, phrase_limit=10)
        if audio is None:
            return ""
            
        text = self._transcribe(audio)
        
        if text:
            print(f"👤 You said: '{text}'")
        
        return text or ""

    def _capture_audio(self, timeout=None, phrase_limit=10):
        """
        Capture audio from microphone.
        
        Parameters:
        - timeout: How long to wait for speech to START (None = wait forever)
        - phrase_limit: Max seconds to record once speech starts
        
        CONCEPT: Audio Capture
        sr.Microphone() opens your mic as an audio stream.
        listen() reads audio chunks until:
        - Speech starts (energy goes above threshold)
        - Then silence detected (end of phrase)
        Returns an AudioData object containing raw PCM samples.
        """
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,          # Wait for speech to start
                    phrase_time_limit=phrase_limit  # Max recording length
                )
            return audio
        except sr.WaitTimeoutError:
            return None  # Nobody spoke in time

    def _transcribe(self, audio) -> str:
        """
        Send audio to Google Speech Recognition API.
        
        CONCEPT: Google Speech-to-Text
        - Sends audio as HTTP POST to Google's servers
        - Google runs a neural network (Conformer/RNN-T architecture)
        - Returns JSON: {"result": [{"alternative": [{"transcript": "text"}]}]}
        - We extract just the transcript text
        """
        try:
            text = self.recognizer.recognize_google(audio, language="en-US")
            return text
        except sr.UnknownValueError:
            # Audio was captured but couldn't be understood
            return ""
        except sr.RequestError as e:
            # Network error or API issue
            print(f"⚠️ Speech API error: {e}")
            return ""