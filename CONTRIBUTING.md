# Contributing to HotkeyForge

First off, thank you for considering contributing to HotkeyForge! It's people like you that make HotkeyForge such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by the HotkeyForge Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed and what you expected**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain the expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Include screenshots and animated GIFs in your pull request whenever possible
- Follow the Python style guide (PEP 8)
- Include tests for new features
- Update documentation for API changes

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- git

### Setup Steps

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/HotkeyForge.git
   cd HotkeyForge
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\activate  # Windows
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
5. Run tests:
   ```bash
   pytest
   ```

## Coding Standards

### Python Style Guide

- Follow PEP 8 conventions
- Use 4 spaces for indentation
- Maximum line length is 100 characters
- Use meaningful variable and function names

### Commit Messages

We follow the Conventional Commits specification:

- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation only changes
- `style:` Changes that do not affect the meaning of the code
- `refactor:` A code change that neither fixes a bug nor adds a feature
- `test:` Adding missing tests or correcting existing tests
- `chore:` Changes to the build process or auxiliary tools

Example:
```
feat: add support for custom hotkey handlers

This commit adds the ability to register custom Python functions
as hotkey handlers, allowing for more flexible automation.

Closes #123
```

### Testing

- Write unit tests for all new functionality
- Ensure all tests pass before submitting a PR
- Aim for high code coverage (80%+)

Run tests:
```bash
pytest
pytest --cov=hotkeyforge  # with coverage
```

## Project Structure

```
HotkeyForge/
├── src/hotkeyforge/       # Main source code
│   ├── __init__.py
│   ├── cli.py             # CLI commands
│   ├── core.py            # Core functionality
│   └── constants.py       # Constants and defaults
├── tests/                 # Test files
├── docs/                  # Documentation
├── pyproject.toml         # Project configuration
└── README.md              # Project readme
```

## Additional Notes

### Issue and Pull Request Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed

## Questions?

Feel free to open an issue with the `question` label or reach out to the maintainers.

Thank you for your contributions! 🎉
