"""
Constants and default configurations for HotkeyForge.
"""

import os
from pathlib import Path
from typing import Dict, List

# Application info
APP_NAME = "HotkeyForge"
APP_VERSION = "1.0.0"
APP_AUTHOR = "HotkeyForge Team"

# Paths
CONFIG_DIR = Path.home() / ".config" / "hotkeyforge"
DATA_DIR = Path.home() / ".local" / "share" / "hotkeyforge"
CACHE_DIR = Path.home() / ".cache" / "hotkeyforge"

DEFAULT_CONFIG_PATH = CONFIG_DIR / "config.yaml"
DEFAULT_LOG_PATH = DATA_DIR / "hotkeyforge.log"
DEFAULT_STATS_PATH = DATA_DIR / "statistics.json"
DEFAULT_TEMPLATES_PATH = CONFIG_DIR / "templates.yaml"

# Modifier keys
MODIFIER_KEYS = {
    "ctrl": "ctrl",
    "alt": "alt",
    "shift": "shift",
    "cmd": "cmd",
    "win": "cmd",  # Windows key alias
    "super": "cmd",  # Linux super key alias
    "meta": "cmd",
}

# Special keys mapping
SPECIAL_KEYS = {
    "space": "space",
    "tab": "tab",
    "enter": "enter",
    "return": "enter",
    "escape": "escape",
    "esc": "escape",
    "backspace": "backspace",
    "delete": "delete",
    "del": "delete",
    "insert": "insert",
    "ins": "insert",
    "home": "home",
    "end": "end",
    "page_up": "page_up",
    "page_down": "page_down",
    "up": "up",
    "down": "down",
    "left": "left",
    "right": "right",
    "f1": "f1",
    "f2": "f2",
    "f3": "f3",
    "f4": "f4",
    "f5": "f5",
    "f6": "f6",
    "f7": "f7",
    "f8": "f8",
    "f9": "f9",
    "f10": "f10",
    "f11": "f11",
    "f12": "f12",
    "caps_lock": "caps_lock",
    "num_lock": "num_lock",
    "scroll_lock": "scroll_lock",
    "print_screen": "print_screen",
    "pause": "pause",
}

# Default hotkey templates
DEFAULT_TEMPLATES: Dict[str, Dict] = {
    "window_management": {
        "description": "Window management shortcuts",
        "hotkeys": {
            "maximize_window": {
                "keys": "win+up",
                "description": "Maximize current window",
                "action": "system",
            },
            "minimize_window": {
                "keys": "win+down",
                "description": "Minimize current window",
                "action": "system",
            },
            "close_window": {
                "keys": "alt+f4",
                "description": "Close current window",
                "action": "system",
            },
        },
    },
    "clipboard": {
        "description": "Clipboard management shortcuts",
        "hotkeys": {
            "copy": {
                "keys": "ctrl+c",
                "description": "Copy to clipboard",
                "action": "system",
            },
            "paste": {
                "keys": "ctrl+v",
                "description": "Paste from clipboard",
                "action": "system",
            },
            "cut": {
                "keys": "ctrl+x",
                "description": "Cut to clipboard",
                "action": "system",
            },
        },
    },
    "developer": {
        "description": "Developer productivity shortcuts",
        "hotkeys": {
            "open_terminal": {
                "keys": "ctrl+alt+t",
                "description": "Open terminal",
                "action": "command",
                "command": "gnome-terminal" if os.name != "nt" else "cmd",
            },
            "screenshot": {
                "keys": "print_screen",
                "description": "Take screenshot",
                "action": "command",
                "command": "gnome-screenshot" if os.name != "nt" else "snippingtool",
            },
        },
    },
    "media": {
        "description": "Media control shortcuts",
        "hotkeys": {
            "play_pause": {
                "keys": "media_play_pause",
                "description": "Play/Pause media",
                "action": "media",
            },
            "next_track": {
                "keys": "media_next",
                "description": "Next track",
                "action": "media",
            },
            "prev_track": {
                "keys": "media_previous",
                "description": "Previous track",
                "action": "media",
            },
            "volume_up": {
                "keys": "volume_up",
                "description": "Increase volume",
                "action": "media",
            },
            "volume_down": {
                "keys": "volume_down",
                "description": "Decrease volume",
                "action": "media",
            },
        },
    },
}

# Default configuration
DEFAULT_CONFIG: Dict = {
    "version": APP_VERSION,
    "settings": {
        "auto_start": False,
        "show_notifications": True,
        "log_enabled": True,
        "log_level": "INFO",
        "conflict_detection": True,
        "stats_enabled": True,
    },
    "hotkeys": {},
    "profiles": {
        "default": {
            "description": "Default profile",
            "enabled": True,
            "hotkeys": [],
        }
    },
    "active_profile": "default",
}

# Action types
ACTION_TYPES = [
    "command",  # Execute a shell command
    "script",  # Run a script file
    "url",  # Open a URL
    "system",  # System action (handled by OS)
    "media",  # Media control
    "custom",  # Custom Python function
]

# Supported platforms
SUPPORTED_PLATFORMS = ["windows", "linux", "darwin"]

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_CONFIG_ERROR = 2
EXIT_PERMISSION_ERROR = 3
EXIT_KEYBOARD_INTERRUPT = 130
