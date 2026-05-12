# ============================================================
#  MAIN.PY — JARVIS ENTRY POINT
#  This is where everything starts and the main loop runs
# ============================================================

import sys
import time
import config

# Import our modules
from speaker import Speaker
from listener import Listener
from commandhandler import CommandHandler

# Optional: face recognition (only if enabled in config)
if config.FACE_RECOGNITION_ENABLED:
    from facerecognition import FaceRecognizer


def startup_sequence(speaker: Speaker, listener: Listener):
    """
    Boot sequence — optional face recognition to verify user,
    then greet them.
    """
    print("\n" + "="*50)
    print("        J.A.R.V.I.S  STARTING UP")
    print("="*50 + "\n")
    
    # Face recognition greeting
    if config.FACE_RECOGNITION_ENABLED:
        try:
            recognizer = FaceRecognizer()
            
            if recognizer.known_face_encodings:
                speaker.speak("Activating facial recognition. Please look at the camera.")
                
                is_authorized, name = recognizer.verify_user()
                
                if is_authorized:
                    speaker.speak(f"Identity confirmed. Welcome back, {name}. How can I assist you?")
                else:
                    speaker.speak("Face not recognized. Proceeding as guest. How can I help?")
            else:
                speaker.speak(f"All systems online. How can I assist you today, {config.USER_NAME}?")
                
        except Exception as e:
            print(f"⚠️ Face recognition error: {e}")
            speaker.speak(f"Jarvis online. Hello, {config.USER_NAME}.")
    else:
        speaker.speak(f"Jarvis online. Hello, {config.USER_NAME}.")


def main():
    """
    MAIN LOOP — The heart of Jarvis.
    
    CONCEPT: Event Loop
    Most programs (games, GUIs, voice assistants) use an "event loop" —
    an infinite loop that:
    1. Waits for an event (wake word, click, keypress)
    2. Processes the event
    3. Goes back to waiting
    
    Our event loop:
    ┌──────────────────────────────────┐
    │  Wait for "Jarvis" wake word     │
    │         ↓                        │
    │  Play activation sound/response  │
    │         ↓                        │
    │  Listen for command              │
    │         ↓                        │
    │  Process command (route it)      │
    │         ↓                        │
    │  Speak the response              │
    │         ↓                        │
    │  Loop back to top                │
    └──────────────────────────────────┘
    
    CONCEPT: State Machine
    Jarvis has two states:
    - SLEEPING: listening only for wake word (low CPU usage)
    - ACTIVE: processing your command
    """
    
    # Initialize all components
    print("🔧 Initializing Jarvis components...")
    
    speaker = Speaker()
    listener = Listener()
    handler = CommandHandler()
    
    # Run startup sequence (face recognition + greeting)
    startup_sequence(speaker, listener)
    
    # ── MAIN LOOP ──────────────────────────────────────────────
    print("\n🚀 Jarvis is running. Press Ctrl+C to stop.\n")
    
    while True:  # This loop runs FOREVER until break or Ctrl+C
        try:
            
            # ── PHASE 1: SLEEP — Wait for wake word ──────────────
            listener.listen_for_wake_word()
            
            # ── PHASE 2: ACTIVE — Process command ────────────────
            
            # Play activation chime / acknowledgment
            speaker.speak("Yes?")
            
            # Listen for the actual command
            command = listener.listen_for_command()
            
            if not command:
                speaker.speak("I didn't hear anything. I'll go back to sleep.")
                continue  # Go back to wake word listening
            
            # ── PHASE 3: PROCESS ─────────────────────────────────
            print(f"\n⚡ Processing: '{command}'")
            
            response = handler.process(command)
            
            # Handle special signals
            if response == "SHUTDOWN":
                speaker.speak(f"Shutting down. Goodbye, {config.USER_NAME}!")
                break  # Exit the while loop → program ends
            
            if response == "SLEEP":
                speaker.speak("Going to sleep. Call me when you need me.")
                continue  # Go straight back to wake word detection
            
            # ── PHASE 4: RESPOND ─────────────────────────────────
            speaker.speak(response)
            
            # Small pause before going back to sleep
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            # User pressed Ctrl+C
            print("\n\n⚠️ Keyboard interrupt received")
            speaker.speak("Powering down. Goodbye!")
            break
            
        except Exception as e:
            # Catch any unexpected errors so Jarvis keeps running
            print(f"❌ Unexpected error: {e}")
            try:
                speaker.speak("I encountered an error. Let me try again.")
            except:
                pass
            time.sleep(1)  # Brief pause before retrying
    
    print("\n✅ Jarvis shut down cleanly.")
    sys.exit(0)


# ── ENTRY POINT ────────────────────────────────────────────
# This block only runs when you execute: python main.py
# NOT when this file is imported by another file
# This is a Python best practice for all main scripts
if __name__ == "__main__":
    main()