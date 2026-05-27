"""Test suite for HotkeyForge."""

import pytest
from pathlib import Path
import tempfile
import yaml

from hotkeyforge.core import Hotkey, HotkeyConfig, HotkeyManager
from hotkeyforge.constants import DEFAULT_CONFIG


class TestHotkey:
    """Tests for Hotkey class."""
    
    def test_hotkey_creation(self):
        """Test basic hotkey creation."""
        hotkey = Hotkey(
            name="test_hotkey",
            keys="ctrl+alt+t",
            description="Test hotkey",
            action="command",
            command="echo test",
        )
        
        assert hotkey.name == "test_hotkey"
        assert hotkey.keys == "ctrl+alt+t"
        assert hotkey.description == "Test hotkey"
        assert hotkey.action == "command"
        assert hotkey.command == "echo test"
        assert hotkey.enabled is True
    
    def test_hotkey_to_dict(self):
        """Test hotkey serialization."""
        hotkey = Hotkey(
            name="test",
            keys="ctrl+c",
            description="Copy",
        )
        
        data = hotkey.to_dict()
        
        assert data["name"] == "test"
        assert data["keys"] == "ctrl+c"
        assert data["description"] == "Copy"
        assert data["enabled"] is True
    
    def test_hotkey_from_dict(self):
        """Test hotkey deserialization."""
        data = {
            "name": "test",
            "keys": "ctrl+v",
            "description": "Paste",
            "action": "command",
            "command": "xclip -o",
            "enabled": False,
        }
        
        hotkey = Hotkey.from_dict(data)
        
        assert hotkey.name == "test"
        assert hotkey.keys == "ctrl+v"
        assert hotkey.enabled is False
    
    def test_parse_keys_simple(self):
        """Test simple key parsing."""
        hotkey = Hotkey(name="test", keys="a")
        modifiers, key = hotkey.parse_keys()
        
        assert modifiers == set()
        assert key == "a"
    
    def test_parse_keys_with_modifiers(self):
        """Test key parsing with modifiers."""
        hotkey = Hotkey(name="test", keys="ctrl+alt+delete")
        modifiers, key = hotkey.parse_keys()
        
        assert "ctrl" in modifiers
        assert "alt" in modifiers
        assert key == "delete"
    
    def test_parse_keys_case_insensitive(self):
        """Test case-insensitive key parsing."""
        hotkey = Hotkey(name="test", keys="CTRL+ALT+T")
        modifiers, key = hotkey.parse_keys()
        
        assert "ctrl" in modifiers
        assert "alt" in modifiers
        assert key == "t"


class TestHotkeyConfig:
    """Tests for HotkeyConfig class."""
    
    def test_config_creation(self):
        """Test config creation with temp file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = HotkeyConfig(config_path=config_path)
            
            assert config.config is not None
            assert config_path.exists()
    
    def test_add_hotkey(self):
        """Test adding a hotkey."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = HotkeyConfig(config_path=config_path)
            
            hotkey = Hotkey(name="test", keys="ctrl+t", description="Test")
            result = config.add_hotkey(hotkey)
            
            assert result is True
            assert "test" in config.hotkeys
    
    def test_add_duplicate_hotkey(self):
        """Test adding duplicate hotkey."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = HotkeyConfig(config_path=config_path)
            
            hotkey = Hotkey(name="test", keys="ctrl+t")
            config.add_hotkey(hotkey)
            
            # Try to add duplicate
            result = config.add_hotkey(hotkey)
            assert result is False
    
    def test_remove_hotkey(self):
        """Test removing a hotkey."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = HotkeyConfig(config_path=config_path)
            
            hotkey = Hotkey(name="test", keys="ctrl+t")
            config.add_hotkey(hotkey)
            
            result = config.remove_hotkey("test")
            assert result is True
            assert "test" not in config.hotkeys
    
    def test_remove_nonexistent_hotkey(self):
        """Test removing non-existent hotkey."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = HotkeyConfig(config_path=config_path)
            
            result = config.remove_hotkey("nonexistent")
            assert result is False
    
    def test_update_hotkey(self):
        """Test updating a hotkey."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = HotkeyConfig(config_path=config_path)
            
            hotkey = Hotkey(name="test", keys="ctrl+t", description="Original")
            config.add_hotkey(hotkey)
            
            result = config.update_hotkey("test", {"description": "Updated"})
            assert result is True
            assert config.hotkeys["test"].description == "Updated"
    
    def test_detect_conflicts(self):
        """Test conflict detection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = HotkeyConfig(config_path=config_path)
            
            # Add two hotkeys with same keys
            hotkey1 = Hotkey(name="copy1", keys="ctrl+c")
            hotkey2 = Hotkey(name="copy2", keys="ctrl+c")
            config.add_hotkey(hotkey1)
            config.add_hotkey(hotkey2)
            
            conflicts = config.detect_conflicts()
            
            assert "ctrl+c" in conflicts
            assert len(conflicts["ctrl+c"]) == 2
    
    def test_list_hotkeys(self):
        """Test listing hotkeys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = HotkeyConfig(config_path=config_path)
            
            hotkey1 = Hotkey(name="test1", keys="ctrl+t", profile="default")
            hotkey2 = Hotkey(name="test2", keys="ctrl+s", profile="work")
            config.add_hotkey(hotkey1)
            config.add_hotkey(hotkey2)
            
            all_hotkeys = config.list_hotkeys()
            assert len(all_hotkeys) == 2
            
            default_hotkeys = config.list_hotkeys(profile="default")
            assert len(default_hotkeys) == 1


class TestHotkeyManager:
    """Tests for HotkeyManager class."""
    
    def test_manager_creation(self):
        """Test manager creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = HotkeyConfig(config_path=config_path)
            manager = HotkeyManager(config=config)
            
            assert manager.config is not None
            assert not manager.is_running()
    
    def test_get_statistics(self):
        """Test statistics retrieval."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = HotkeyConfig(config_path=config_path)
            manager = HotkeyManager(config=config)
            
            hotkey = Hotkey(name="test", keys="ctrl+t", trigger_count=5)
            config.add_hotkey(hotkey)
            
            stats = manager.get_statistics()
            
            assert stats["total_hotkeys"] == 1
            assert stats["total_triggers"] == 5
    
    def test_apply_template(self):
        """Test template application."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = HotkeyConfig(config_path=config_path)
            manager = HotkeyManager(config=config)
            
            result = manager.apply_template("clipboard")
            assert result is True
            
            # Check that template hotkeys were added
            assert len(config.hotkeys) > 0
    
    def test_apply_nonexistent_template(self):
        """Test applying non-existent template."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config = HotkeyConfig(config_path=config_path)
            manager = HotkeyManager(config=config)
            
            result = manager.apply_template("nonexistent")
            assert result is False
    
    def test_export_import_config(self):
        """Test config export and import."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            export_path = Path(tmpdir) / "export.yaml"
            config = HotkeyConfig(config_path=config_path)
            manager = HotkeyManager(config=config)
            
            # Add a hotkey
            hotkey = Hotkey(name="test", keys="ctrl+t", description="Test")
            config.add_hotkey(hotkey)
            
            # Export
            result = manager.export_config(export_path)
            assert result is True
            assert export_path.exists()
            
            # Create new config and import
            new_config_path = Path(tmpdir) / "new_config.yaml"
            new_config = HotkeyConfig(config_path=new_config_path)
            new_manager = HotkeyManager(config=new_config)
            
            result = new_manager.import_config(export_path)
            assert result is True
            assert "test" in new_config.hotkeys


class TestCLI:
    """Tests for CLI commands."""
    
    def test_version(self, capsys):
        """Test version flag."""
        from click.testing import CliRunner
        from hotkeyforge.cli import main
        
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        
        assert result.exit_code == 0
        assert "HotkeyForge version" in result.output
    
    def test_help(self):
        """Test help command."""
        from click.testing import CliRunner
        from hotkeyforge.cli import main
        
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        
        assert result.exit_code == 0
        assert "HotkeyForge" in result.output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
