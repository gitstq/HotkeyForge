"""
HotkeyForge - A powerful cross-platform hotkey management CLI tool.

This package provides a comprehensive solution for managing, configuring,
and monitoring system-wide hotkeys with advanced features like conditional
triggers, conflict detection, and usage statistics.
"""

__version__ = "1.0.0"
__author__ = "HotkeyForge Team"
__license__ = "MIT"

from hotkeyforge.core import HotkeyManager, HotkeyConfig
from hotkeyforge.constants import DEFAULT_CONFIG_PATH, DEFAULT_LOG_PATH

__all__ = [
    "HotkeyManager",
    "HotkeyConfig",
    "DEFAULT_CONFIG_PATH",
    "DEFAULT_LOG_PATH",
]
