# ============================================================
#  SYSTEM CONTROL MODULE
#  Handles system-level commands: time, date, volume, shutdown, etc.
# ============================================================

import datetime
import platform
import subprocess
import os

class SystemControl:
    """
    Controls OS-level functions.
    Uses Python's built-in modules + OS-specific shell commands.
    
    CONCEPT: platform module
    platform.system() returns your OS: "Windows", "Darwin", "Linux"
    This lets us write cross-platform code that picks the right
    command for each operating system.
    """

    def __init__(self):
        self.os_type = platform.system()

    def get_time(self) -> str:
        """
        Get current time.
        
        CONCEPT: datetime module
        datetime.datetime.now() returns the current local time.
        .strftime() formats it using format codes:
        %I = 12-hour hour, %M = minutes, %p = AM/PM
        """
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")  # e.g., "03:45 PM"
        return f"The current time is {time_str}"

    def get_date(self) -> str:
        """Get today's date."""
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")  # e.g., "Monday, May 12, 2025"
        return f"Today is {date_str}"

    def get_day(self) -> str:
        """Get day of week."""
        day = datetime.datetime.now().strftime("%A")
        return f"Today is {day}"

    def set_volume(self, level: int) -> str:
        """
        Set system volume (0-100).
        Uses different commands per OS.
        
        CONCEPT: Shell Commands via subprocess
        We run OS-specific commands:
        - Windows: PowerShell script to set audio
        - Mac: osascript (AppleScript) to control audio
        - Linux: amixer (ALSA mixer) command
        """
        level = max(0, min(100, level))  # Clamp between 0-100
        
        try:
            if self.os_type == "Windows":
                # PowerShell command to set volume
                script = f"(New-Object -ComObject WScript.Shell).SendKeys([char]174)"
                # More reliable Windows volume control:
                cmd = f"""powershell -c "$vol = {level}/100; 
                    Add-Type -TypeDefinition 'using System.Runtime.InteropServices; 
                    public class AudioManager {{
                        [DllImport(\"winmm.dll\")] 
                        public static extern int waveOutSetVolume(IntPtr h, uint v);
                    }}'; 
                    [AudioManager]::waveOutSetVolume([IntPtr]::Zero, [uint]($vol * 0xFFFF + $vol * 0xFFFF * 0x10000))"
                """
                subprocess.run(cmd, shell=True, capture_output=True)
                
            elif self.os_type == "Darwin":  # Mac
                # osascript runs AppleScript commands
                subprocess.run(f"osascript -e 'set volume output volume {level}'", 
                             shell=True, capture_output=True)
                
            elif self.os_type == "Linux":
                subprocess.run(f"amixer sset Master {level}%", 
                             shell=True, capture_output=True)
            
            return f"Volume set to {level} percent"
        except Exception as e:
            return f"Couldn't set volume: {e}"

    def shutdown(self) -> str:
        """Shutdown the computer."""
        if self.os_type == "Windows":
            subprocess.run("shutdown /s /t 5", shell=True)
            return "Shutting down in 5 seconds. Goodbye!"
        elif self.os_type == "Darwin":
            subprocess.run("sudo shutdown -h +1", shell=True)
            return "Shutting down in 1 minute."
        else:
            subprocess.run("sudo shutdown -h now", shell=True)
            return "Shutting down now."

    def restart(self) -> str:
        """Restart the computer."""
        if self.os_type == "Windows":
            subprocess.run("shutdown /r /t 5", shell=True)
        elif self.os_type == "Darwin":
            subprocess.run("sudo shutdown -r now", shell=True)
        else:
            subprocess.run("sudo reboot", shell=True)
        return "Restarting. See you on the other side!"

    def handle_command(self, command: str) -> str | None:
        """
        Parse system commands from voice input.
        Returns response string if handled, None if not a system command.
        """
        cmd = command.lower().strip()
        
        # Time/date queries
        if any(word in cmd for word in ["what time", "current time", "time is it"]):
            return self.get_time()
        
        if any(word in cmd for word in ["what date", "today's date", "what day"]):
            return self.get_date()
        
        if "day is it" in cmd or "day today" in cmd:
            return self.get_day()
        
        # Volume control
        if "volume" in cmd:
            # Try to extract a number from the command
            words = cmd.split()
            for word in words:
                if word.isdigit():
                    return self.set_volume(int(word))
            if "up" in cmd:
                return self.set_volume(80)
            if "down" in cmd or "low" in cmd:
                return self.set_volume(30)
            if "mute" in cmd:
                return self.set_volume(0)
        
        # System control
        if "shutdown" in cmd or "shut down" in cmd:
            return self.shutdown()
        
        if "restart" in cmd or "reboot" in cmd:
            return self.restart()
        
        return None  # Not a system command