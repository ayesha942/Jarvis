# ============================================================
#  APP LAUNCHER MODULE
#  Opens applications and websites by voice command
# ============================================================

import subprocess
import webbrowser
import platform
import config

class AppLauncher:
    """
    Handles opening apps and websites.
    
    CONCEPT: subprocess
    subprocess.Popen() spawns a NEW process (program) from Python.
    Your OS manages processes — each running program is a process.
    Python's subprocess module lets you start, stop, and communicate
    with other processes.
    
    CONCEPT: webbrowser
    Python's built-in webbrowser module opens URLs in your 
    default browser. It figures out which browser to use 
    automatically (Chrome, Firefox, Edge, etc.)
    """

    def __init__(self):
        self.os_type = platform.system()  # "Windows", "Darwin" (Mac), "Linux"

    def open_website(self, url: str) -> str:
        """
        Open a URL in the default web browser.
        webbrowser.open() is cross-platform — works on Windows, Mac, Linux.
        """
        try:
            webbrowser.open(url)
            return f"Opening {url}"
        except Exception as e:
            return f"Couldn't open website: {e}"

    def open_app(self, app_name: str) -> str:
        """
        Open a native application.
        
        CONCEPT: Cross-Platform Commands
        Different OS use different commands to launch apps:
        - Windows: just the .exe name or full path
        - Mac: "open -a AppName"
        - Linux: just the binary name (e.g., "gedit", "firefox")
        """
        app_name_lower = app_name.lower()
        
        # Check config map first
        if app_name_lower in config.APP_MAP:
            app_command = config.APP_MAP[app_name_lower]
            return self._launch(app_command)
        
        # Check website map
        if app_name_lower in config.WEBSITE_MAP:
            return self.open_website(config.WEBSITE_MAP[app_name_lower])
        
        # Try to open it directly by name
        return self._launch(app_name)

    def _launch(self, command: str) -> str:
        """
        Use subprocess to launch a program.
        
        Popen vs run:
        - subprocess.Popen() = starts process, DOESN'T wait for it to finish
          (good for apps — you want them to stay open)
        - subprocess.run() = starts process, WAITS for it to finish
          (good for commands where you need the output)
        
        shell=True means the command goes through your OS shell
        (cmd.exe on Windows, bash on Linux/Mac) which lets it find
        apps in your PATH environment variable.
        """
        try:
            if self.os_type == "Windows":
                subprocess.Popen(command, shell=True)
            elif self.os_type == "Darwin":  # Mac
                subprocess.Popen(f"open -a '{command}'", shell=True)
            else:  # Linux
                subprocess.Popen(command, shell=True)
            return f"Opening {command}"
        except Exception as e:
            return f"Couldn't open {command}: {e}"

    def handle_command(self, command: str) -> str | None:
        """
        Parse a voice command and decide what to open.
        Returns response string if handled, None if not our job.
        
        Examples:
        "open youtube" → opens youtube.com
        "open calculator" → opens calc.exe
        "open spotify" → tries to launch Spotify
        """
        command_lower = command.lower()
        
        # Must start with "open"
        if not command_lower.startswith("open"):
            return None
        
        # Extract what to open (everything after "open ")
        target = command_lower.replace("open", "").strip()
        
        if not target:
            return "What would you like me to open?"
        
        # Check websites first
        for keyword, url in config.WEBSITE_MAP.items():
            if keyword in target:
                self.open_website(url)
                return f"Opening {keyword} for you."
        
        # Check apps
        for keyword, app in config.APP_MAP.items():
            if keyword in target:
                self._launch(app)
                return f"Opening {keyword}."
        
        # Try opening whatever they said directly
        self._launch(target)
        return f"Trying to open {target}."