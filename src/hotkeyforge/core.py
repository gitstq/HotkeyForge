"""
Core module for HotkeyForge - Hotkey management and configuration.
"""

import json
import logging
import os
import subprocess
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

import yaml

from hotkeyforge.constants import (
    ACTION_TYPES,
    DEFAULT_CONFIG,
    DEFAULT_CONFIG_PATH,
    DEFAULT_LOG_PATH,
    DEFAULT_STATS_PATH,
    DEFAULT_TEMPLATES,
    MODIFIER_KEYS,
    SPECIAL_KEYS,
)


class HotkeyAction(Enum):
    """Enumeration of hotkey action types."""
    COMMAND = "command"
    SCRIPT = "script"
    URL = "url"
    SYSTEM = "system"
    MEDIA = "media"
    CUSTOM = "custom"


@dataclass
class Hotkey:
    """Represents a single hotkey configuration."""
    name: str
    keys: str
    description: str = ""
    action: str = "command"
    command: Optional[str] = None
    script: Optional[str] = None
    url: Optional[str] = None
    enabled: bool = True
    profile: str = "default"
    conditions: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_triggered: Optional[str] = None
    trigger_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert hotkey to dictionary."""
        return {
            "name": self.name,
            "keys": self.keys,
            "description": self.description,
            "action": self.action,
            "command": self.command,
            "script": self.script,
            "url": self.url,
            "enabled": self.enabled,
            "profile": self.profile,
            "conditions": self.conditions,
            "tags": self.tags,
            "created_at": self.created_at,
            "last_triggered": self.last_triggered,
            "trigger_count": self.trigger_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Hotkey":
        """Create hotkey from dictionary."""
        return cls(
            name=data.get("name", ""),
            keys=data.get("keys", ""),
            description=data.get("description", ""),
            action=data.get("action", "command"),
            command=data.get("command"),
            script=data.get("script"),
            url=data.get("url"),
            enabled=data.get("enabled", True),
            profile=data.get("profile", "default"),
            conditions=data.get("conditions", {}),
            tags=data.get("tags", []),
            created_at=data.get("created_at", datetime.now().isoformat()),
            last_triggered=data.get("last_triggered"),
            trigger_count=data.get("trigger_count", 0),
        )

    def parse_keys(self) -> Tuple[Set[str], str]:
        """
        Parse hotkey string into modifiers and main key.
        
        Returns:
            Tuple of (modifiers set, main key)
        """
        parts = self.keys.lower().replace(" ", "").split("+")
        modifiers = set()
        main_key = ""
        
        for part in parts:
            if part in MODIFIER_KEYS:
                modifiers.add(MODIFIER_KEYS[part])
            elif part in SPECIAL_KEYS:
                main_key = SPECIAL_KEYS[part]
            else:
                main_key = part
        
        return modifiers, main_key


class HotkeyConfig:
    """Configuration manager for HotkeyForge."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.config: Dict[str, Any] = {}
        self.hotkeys: Dict[str, Hotkey] = {}
        self._ensure_dirs()
        self.load()
    
    def _ensure_dirs(self) -> None:
        """Ensure configuration directories exist."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> None:
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config = yaml.safe_load(f) or {}
            except Exception as e:
                logging.warning(f"Failed to load config: {e}")
                self.config = DEFAULT_CONFIG.copy()
        else:
            self.config = DEFAULT_CONFIG.copy()
            self.save()
        
        # Load hotkeys
        hotkeys_data = self.config.get("hotkeys", {})
        for name, data in hotkeys_data.items():
            if isinstance(data, dict):
                data["name"] = name
                self.hotkeys[name] = Hotkey.from_dict(data)
    
    def save(self) -> None:
        """Save configuration to file."""
        # Update hotkeys in config
        self.config["hotkeys"] = {
            name: hk.to_dict() for name, hk in self.hotkeys.items()
        }
        
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
    
    def add_hotkey(self, hotkey: Hotkey) -> bool:
        """
        Add a new hotkey.
        
        Args:
            hotkey: Hotkey to add
            
        Returns:
            True if successful, False if hotkey already exists
        """
        if hotkey.name in self.hotkeys:
            return False
        
        self.hotkeys[hotkey.name] = hotkey
        self.save()
        return True
    
    def remove_hotkey(self, name: str) -> bool:
        """
        Remove a hotkey.
        
        Args:
            name: Name of hotkey to remove
            
        Returns:
            True if successful, False if hotkey not found
        """
        if name not in self.hotkeys:
            return False
        
        del self.hotkeys[name]
        self.save()
        return True
    
    def update_hotkey(self, name: str, updates: Dict[str, Any]) -> bool:
        """
        Update an existing hotkey.
        
        Args:
            name: Name of hotkey to update
            updates: Dictionary of updates
            
        Returns:
            True if successful, False if hotkey not found
        """
        if name not in self.hotkeys:
            return False
        
        hotkey = self.hotkeys[name]
        for key, value in updates.items():
            if hasattr(hotkey, key):
                setattr(hotkey, key, value)
        
        self.save()
        return True
    
    def get_hotkey(self, name: str) -> Optional[Hotkey]:
        """
        Get a hotkey by name.
        
        Args:
            name: Name of hotkey
            
        Returns:
            Hotkey if found, None otherwise
        """
        return self.hotkeys.get(name)
    
    def list_hotkeys(self, profile: Optional[str] = None) -> List[Hotkey]:
        """
        List all hotkeys, optionally filtered by profile.
        
        Args:
            profile: Profile to filter by
            
        Returns:
            List of hotkeys
        """
        hotkeys = list(self.hotkeys.values())
        if profile:
            hotkeys = [hk for hk in hotkeys if hk.profile == profile]
        return hotkeys
    
    def detect_conflicts(self) -> Dict[str, List[str]]:
        """
        Detect hotkey conflicts.
        
        Returns:
            Dictionary mapping key combinations to conflicting hotkey names
        """
        key_map: Dict[str, List[str]] = {}
        
        for name, hotkey in self.hotkeys.items():
            if hotkey.enabled:
                keys = hotkey.keys.lower().replace(" ", "")
                if keys not in key_map:
                    key_map[keys] = []
                key_map[keys].append(name)
        
        # Filter to only conflicts
        conflicts = {k: v for k, v in key_map.items() if len(v) > 1}
        return conflicts
    
    def get_settings(self) -> Dict[str, Any]:
        """Get application settings."""
        return self.config.get("settings", DEFAULT_CONFIG["settings"])
    
    def update_settings(self, settings: Dict[str, Any]) -> None:
        """Update application settings."""
        current = self.get_settings()
        current.update(settings)
        self.config["settings"] = current
        self.save()


class HotkeyManager:
    """Manager for hotkey registration and execution."""
    
    def __init__(self, config: Optional[HotkeyConfig] = None):
        """
        Initialize hotkey manager.
        
        Args:
            config: Configuration manager
        """
        self.config = config or HotkeyConfig()
        self.logger = self._setup_logging()
        self._running = False
        self._listener = None
        self._stats_path = DEFAULT_STATS_PATH
        self._custom_handlers: Dict[str, Callable] = {}
        self._pressed_keys: Set[str] = set()
        self._lock = threading.Lock()
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging."""
        logger = logging.getLogger("hotkeyforge")
        logger.setLevel(logging.DEBUG)
        
        # File handler
        DEFAULT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(DEFAULT_LOG_PATH)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def register_custom_handler(self, name: str, handler: Callable) -> None:
        """
        Register a custom hotkey handler.
        
        Args:
            name: Handler name
            handler: Callable to execute
        """
        self._custom_handlers[name] = handler
    
    def execute_hotkey(self, hotkey: Hotkey) -> bool:
        """
        Execute a hotkey action.
        
        Args:
            hotkey: Hotkey to execute
            
        Returns:
            True if successful, False otherwise
        """
        if not hotkey.enabled:
            return False
        
        try:
            # Update statistics
            hotkey.last_triggered = datetime.now().isoformat()
            hotkey.trigger_count += 1
            self.config.save()
            
            self.logger.info(f"Executing hotkey: {hotkey.name}")
            
            if hotkey.action == "command" and hotkey.command:
                subprocess.Popen(
                    hotkey.command,
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return True
            
            elif hotkey.action == "script" and hotkey.script:
                script_path = Path(hotkey.script)
                if script_path.exists():
                    subprocess.Popen(
                        [str(script_path)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    return True
            
            elif hotkey.action == "url" and hotkey.url:
                import webbrowser
                webbrowser.open(hotkey.url)
                return True
            
            elif hotkey.action == "custom":
                handler = self._custom_handlers.get(hotkey.name)
                if handler:
                    handler()
                    return True
            
            self.logger.warning(f"Unknown action type: {hotkey.action}")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to execute hotkey {hotkey.name}: {e}")
            return False
    
    def _on_press(self, key) -> None:
        """Handle key press event."""
        try:
            key_name = str(key).lower().replace("key.", "")
            
            with self._lock:
                self._pressed_keys.add(key_name)
                self._check_hotkeys()
                
        except Exception as e:
            self.logger.error(f"Error in key press handler: {e}")
    
    def _on_release(self, key) -> None:
        """Handle key release event."""
        try:
            key_name = str(key).lower().replace("key.", "")
            
            with self._lock:
                self._pressed_keys.discard(key_name)
                
        except Exception as e:
            self.logger.error(f"Error in key release handler: {e}")
    
    def _check_hotkeys(self) -> None:
        """Check if any hotkey combinations are triggered."""
        for name, hotkey in self.config.hotkeys.items():
            if not hotkey.enabled:
                continue
            
            modifiers, main_key = hotkey.parse_keys()
            
            # Check if all modifiers are pressed
            if modifiers.issubset(self._pressed_keys):
                # Check if main key is pressed
                if main_key in self._pressed_keys:
                    # Execute in separate thread to avoid blocking
                    threading.Thread(
                        target=self.execute_hotkey,
                        args=(hotkey,),
                        daemon=True,
                    ).start()
    
    def start(self) -> None:
        """Start hotkey listener."""
        if self._running:
            return
        
        try:
            from pynput import keyboard
            
            self._listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release,
            )
            self._listener.start()
            self._running = True
            self.logger.info("Hotkey listener started")
            
        except ImportError:
            self.logger.error("pynput not installed. Install with: pip install pynput")
        except Exception as e:
            self.logger.error(f"Failed to start listener: {e}")
    
    def stop(self) -> None:
        """Stop hotkey listener."""
        if not self._running:
            return
        
        if self._listener:
            self._listener.stop()
            self._listener = None
        
        self._running = False
        self.logger.info("Hotkey listener stopped")
    
    def is_running(self) -> bool:
        """Check if listener is running."""
        return self._running
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get hotkey usage statistics.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            "total_hotkeys": len(self.config.hotkeys),
            "enabled_hotkeys": sum(1 for hk in self.config.hotkeys.values() if hk.enabled),
            "total_triggers": sum(hk.trigger_count for hk in self.config.hotkeys.values()),
            "hotkeys": {},
        }
        
        for name, hotkey in self.config.hotkeys.items():
            stats["hotkeys"][name] = {
                "trigger_count": hotkey.trigger_count,
                "last_triggered": hotkey.last_triggered,
            }
        
        return stats
    
    def save_statistics(self) -> None:
        """Save statistics to file."""
        stats = self.get_statistics()
        self._stats_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self._stats_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
    
    def apply_template(self, template_name: str) -> bool:
        """
        Apply a hotkey template.
        
        Args:
            template_name: Name of template to apply
            
        Returns:
            True if successful, False if template not found
        """
        if template_name not in DEFAULT_TEMPLATES:
            return False
        
        template = DEFAULT_TEMPLATES[template_name]
        for name, data in template.get("hotkeys", {}).items():
            if name not in self.config.hotkeys:
                hotkey = Hotkey(
                    name=name,
                    keys=data.get("keys", ""),
                    description=data.get("description", ""),
                    action=data.get("action", "command"),
                    command=data.get("command"),
                    tags=[template_name],
                )
                self.config.add_hotkey(hotkey)
        
        return True
    
    def export_config(self, path: Path) -> bool:
        """
        Export configuration to file.
        
        Args:
            path: Export path
            
        Returns:
            True if successful
        """
        try:
            export_data = {
                "version": self.config.config.get("version"),
                "settings": self.config.get_settings(),
                "hotkeys": {name: hk.to_dict() for name, hk in self.config.hotkeys.items()},
            }
            
            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(export_data, f, default_flow_style=False, allow_unicode=True)
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to export config: {e}")
            return False
    
    def import_config(self, path: Path) -> bool:
        """
        Import configuration from file.
        
        Args:
            path: Import path
            
        Returns:
            True if successful
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                import_data = yaml.safe_load(f)
            
            if import_data:
                # Merge settings
                if "settings" in import_data:
                    self.config.update_settings(import_data["settings"])
                
                # Import hotkeys
                for name, data in import_data.get("hotkeys", {}).items():
                    if isinstance(data, dict):
                        data["name"] = name
                        hotkey = Hotkey.from_dict(data)
                        self.config.hotkeys[name] = hotkey
                
                self.config.save()
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to import config: {e}")
            return False
