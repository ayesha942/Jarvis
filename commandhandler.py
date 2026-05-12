# ============================================================
#  COMMAND HANDLER (The Router)
#  Decides WHICH module handles each voice command
#  Think of it as the "traffic controller" of Jarvis
# ============================================================

from applauncher import AppLauncher
from systemcontrol import SystemControl
from brain import Brain

class CommandHandler:
    """
    CONCEPT: Command Pattern (Design Pattern)
    Instead of one giant if-elif chain, we have specialized modules.
    CommandHandler tries each module in order until one handles the command.
    This is the "Chain of Responsibility" design pattern.
    
    Order of priority:
    1. System commands (time, volume, shutdown)
    2. App/website launching  
    3. Special built-in commands (clear memory, help)
    4. Everything else → Claude AI
    
    This means if you say "open the time machine movie", 
    system_control won't claim it (no "time is it" keyword),
    app_launcher will open it (starts with "open"),
    and AI never sees it.
    """

    def __init__(self):
        self.app_launcher = AppLauncher()
        self.system_control = SystemControl()
        self.brain = Brain()
        
        print("⚙️ Command handler ready")

    def process(self, command: str) -> str:
        """
        Main routing function.
        Takes a voice command string, returns Jarvis's response string.
        """
        if not command or not command.strip():
            return "I didn't catch that. Could you repeat?"
        
        command = command.strip()
        command_lower = command.lower()
        
        # ── BUILT-IN COMMANDS ──────────────────────────────────
        
        # Stop/exit commands
        if any(word in command_lower for word in ["stop", "exit", "quit", "goodbye", "bye"]):
            return "SHUTDOWN"  # Special signal to main.py
        
        # Sleep/deactivate
        if any(word in command_lower for word in ["go to sleep", "sleep mode", "shut up"]):
            return "SLEEP"  # Signal to go back to wake word listening
        
        # Clear AI memory
        if any(phrase in command_lower for phrase in ["clear memory", "forget everything", "reset"]):
            return self.brain.clear_memory()
        
        # Help command
        if command_lower in ["help", "what can you do", "commands"]:
            return self._get_help()
        
        # ── MODULE ROUTING ─────────────────────────────────────
        
        # Try system control first (time, volume, shutdown)
        response = self.system_control.handle_command(command)
        if response is not None:
            return response
        
        # Try app/website launcher (anything starting with "open")
        response = self.app_launcher.handle_command(command)
        if response is not None:
            return response
        
        # ── AI FALLBACK ────────────────────────────────────────
        # If no module handled it, ask Claude
        return self.brain.ask(command)

    def _get_help(self) -> str:
        return (
            "I can help with several things. "
            "Say 'open' followed by an app or website name to launch it. "
            "Ask me the time, date, or to set the volume. "
            "Or just ask me any question and I'll use my AI to answer."
        )