<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <a href="README.md">English</a> | 
  <a href="README_CN.md">简体中文</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">🔥 HotkeyForge</h1>

<p align="center">
  <strong>A Powerful Cross-Platform Hotkey Management CLI Tool for Developers</strong>
</p>

<p align="center">
  <em>Forge your productivity with customizable system-wide hotkeys</em>
</p>

---

## 🎉 Project Introduction

**HotkeyForge** is a powerful command-line tool designed to help developers and power users manage system-wide hotkeys efficiently. It provides a unified interface to create, configure, and monitor keyboard shortcuts across Windows, Linux, and macOS.

### Why HotkeyForge?

- 🎯 **Unified Management**: Manage all your hotkeys in one place
- ⚡ **Cross-Platform**: Works seamlessly on Windows, Linux, and macOS
- 🔧 **Highly Configurable**: Support for commands, scripts, URLs, and custom actions
- 📊 **Usage Statistics**: Track how often you use each hotkey
- 🛡️ **Conflict Detection**: Automatically detect and warn about conflicting shortcuts
- 📦 **Template System**: Pre-built templates for common use cases

---

## ✨ Core Features

### 🔑 Hotkey Management
- **Add/Remove/Update hotkeys** with simple CLI commands
- Support for **complex key combinations** (Ctrl+Alt+Shift+Key)
- **Enable/disable** hotkeys without deleting them
- **Profile-based organization** for different workflows

### 🚀 Action Types
| Action | Description |
|--------|-------------|
| `command` | Execute shell commands |
| `script` | Run script files |
| `url` | Open URLs in browser |
| `custom` | Custom Python handlers |

### 📊 Statistics & Monitoring
- Track **trigger counts** for each hotkey
- View **last triggered** timestamps
- Export statistics for analysis

### 🛡️ Smart Features
- **Conflict Detection**: Automatically warn when multiple hotkeys share the same keys
- **Template Library**: Pre-configured hotkey sets for common tasks
- **Import/Export**: Backup and restore your configurations

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Install from PyPI
pip install hotkeyforge

# Or install from source
git clone https://github.com/gitstq/HotkeyForge.git
cd HotkeyForge
pip install -e .
```

### Basic Usage

```bash
# Show help
hotkeyforge --help

# Add a new hotkey
hotkeyforge add -n "open_terminal" -k "ctrl+alt+t" -d "Open terminal" -a command -c "gnome-terminal"

# List all hotkeys
hotkeyforge list

# Start the hotkey listener
hotkeyforge start

# Show statistics
hotkeyforge stats

# Detect conflicts
hotkeyforge conflicts
```

---

## 📖 Detailed Usage Guide

### Adding Hotkeys

```bash
# Add a command hotkey
hotkeyforge add -n "screenshot" -k "print_screen" -d "Take screenshot" -a command -c "gnome-screenshot"

# Add a URL hotkey
hotkeyforge add -n "google" -k "ctrl+alt+g" -d "Open Google" -a url -u "https://google.com"

# Add with tags
hotkeyforge add -n "vscode" -k "ctrl+alt+v" -d "Open VS Code" -a command -c "code" -t "dev,editor"
```

### Managing Hotkeys

```bash
# List all hotkeys
hotkeyforge list

# List hotkeys by profile
hotkeyforge list --profile work

# List only enabled hotkeys
hotkeyforge list --enabled

# Update a hotkey
hotkeyforge update "open_terminal" --keys "ctrl+shift+t"

# Disable a hotkey
hotkeyforge update "screenshot" --disabled

# Remove a hotkey
hotkeyforge remove "google"
```

### Using Templates

```bash
# List available templates
hotkeyforge templates

# Apply a template
hotkeyforge apply clipboard
hotkeyforge apply developer
hotkeyforge apply media
```

### Configuration Management

```bash
# View current settings
hotkeyforge config --show

# Enable auto-start
hotkeyforge config --auto-start

# Disable notifications
hotkeyforge config --no-notifications

# Export configuration
hotkeyforge export ~/hotkeyforge_backup.yaml

# Import configuration
hotkeyforge import-config ~/hotkeyforge_backup.yaml
```

---

## 💡 Design Philosophy

### Why We Built HotkeyForge

As developers, we constantly switch between applications, run commands, and perform repetitive tasks. While most operating systems provide basic hotkey functionality, managing them across different applications and workflows is often fragmented and inconsistent.

**HotkeyForge** was created to solve this problem by providing:

1. **Unified Interface**: One tool to manage all your hotkeys
2. **Developer-First Design**: Built for developers who live in the terminal
3. **Extensibility**: Easy to extend with custom actions and handlers
4. **Portability**: Configuration files that work across different machines

### Architecture

```
HotkeyForge
├── CLI Layer (Click-based commands)
├── Core Layer (Hotkey management logic)
│   ├── HotkeyConfig (YAML-based configuration)
│   └── HotkeyManager (Listener and execution)
└── Platform Layer (pynput for cross-platform support)
```

---

## 📦 Build & Deploy

### Building from Source

```bash
# Clone the repository
git clone https://github.com/gitstq/HotkeyForge.git
cd HotkeyForge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Build package
pip install build
python -m build
```

### Creating a Release

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# Upload to PyPI
twine upload dist/*
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation for API changes
- Use conventional commit messages

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [pynput](https://github.com/moses-palmer/pynput) - Cross-platform keyboard monitoring
- [Click](https://github.com/pallets/click) - CLI framework
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal output

---

<p align="center">
  Made with ❤️ by the HotkeyForge Team
</p>
