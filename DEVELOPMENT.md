# Contributing to tts_util

**Thank you for your interest in contributing to tts_util!** This document provides guidelines for contributors.

## Quick Links

- [Getting Started](#getting-started)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Accessibility Focus](#accessibility-focus)

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- pip

### Development Setup

1. **Fork and Clone**

   ```bash
   git clone https://github.com/johnpaulguzman/tts_util.git
   cd tts_util
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install in Development Mode**

   ```bash
   pip install -e ".[test]"
   ```

4. **Verify Installation**
   ```bash
   ttsu --help
   pytest
   ```

## Code Standards

### Python Style

Professionally formatted code. When formatting tools are available:

```bash
# Install black (optional)
pip install black

# Format code
black src/tts_util tests
```

### Type Hints

Encouraged for public APIs:

```python
from typing import Optional, List

def process_text(text: str, language: Optional[str] = None) -> List[str]:
    """Process text into sentences.

    Args:
        text: Input text to process
        language: Optional language code (default: English)

    Returns:
        List of segmented sentences
    """
```

### Imports

Standard organization:

```python
# Standard library
import logging
from pathlib import Path
from typing import Optional

# Third-party
import pynput
import pyttsx3

# Local
from tts_util.core.ports import SpeechPort
from tts_util.adapters.pyttsx3_speech import MultiprocessPyttsx3Speech
```

## Testing

### Running Tests

```bash
# All tests with coverage
pytest

# Specific test file
pytest tests/test_speech_controller.py -v

# Single test
pytest tests/test_speech_controller.py::test_speak -v

# With coverage report
pytest --cov=src/tts_util --cov-report=html
```

### Writing Tests

- **Location**: `tests/` directory
- **Naming**: `test_*.py` for files, `test_*()` for functions
- **Coverage**: 80% minimum required
- **Mocking**: Use `unittest.mock` or pytest fixtures

Example:

```python
def test_text_processor_segments_sentences():
    """Verify TextProcessor creates one object per sentence."""
    processor = TextProcessor()
    text = "Hello world. This is a test."

    segments = processor.segment(text)

    assert len(segments) == 2
    assert "Hello" in segments[0]
    assert "This" in segments[1]
```

### Coverage Requirements

- **Minimum**: 80%
- **Check**: `pytest` automatically
- **Report**: View with `pytest --cov=src/tts_util --cov-report=html`

## Submitting Changes

### Branch Naming

```
feat/custom-hotkeys
feat/voice-selection
fix/clipboard-permission
docs/add-examples
refactor/text-processor
test/increase-coverage
```

### Commit Messages

Use conventional commits:

```
feat: add custom hotkey configuration support

Users can now customize hotkeys via config file.
Supports --config flag to specify custom configuration.

Fixes #45
```

### Pull Request Process

1. **Create Branch**

   ```bash
   git checkout -b feat/my-feature
   ```

2. **Implement Feature**
   - Write code
   - Add tests
   - Update docs if needed

3. **Test Locally**

   ```bash
   pytest                      # Tests pass
   pytest --cov=src/tts_util   # Coverage good (80%+)
   ```

4. **Push and Create PR**

   ```bash
   git push origin feat/my-feature
   ```

5. **Use PR Template**
   - Describe changes
   - Link related issues
   - Mention any accessibility impact

## Accessibility Focus

**tts_util is fundamentally about accessibility.** When contributing:

### Accessibility Checklist

- [ ] **Keyboard Only** - Can users complete the feature without a mouse?
- [ ] **Screen Reader** - Will this work with screen readers?
- [ ] **Audio** - Is audio output clear and helpful?
- [ ] **Latency** - Is response time acceptable for accessibility users?
- [ ] **Fallbacks** - What if audio fails or speech is unavailable?

### Accessibility Testing

```bash
# Test hotkey mode (keyboard-only)
ttsu
```

### Platform-Specific Accessibility

- **Windows**: Test with Narrator (Win + Enter)
- **macOS**: Test with VoiceOver (Cmd + F5)
- **Linux**: Test with Orca or similar

## Reporting Issues

### Bug Reports

Include:

- Python version
- OS and version
- Error traceback
- Steps to reproduce
- Whether other input methods work (hotkeys vs GUI)

### Feature Requests

Explain:

- Use case and benefit
- How it helps accessibility
- Implementation ideas

### Security Issues

See [SECURITY.md](SECURITY.md) for reporting sensitive vulnerabilities.

## Project Structure

```
tts_util/
├── src/tts_util/
│   ├── cli.py              # Command-line interface
│   ├── macro_util.py       # Service composition
│   ├── adapters/           # Implementation classes
│   │   ├── pynput_hotkeys.py
│   │   ├── pynput_text_source.py
│   │   ├── pyttsx3_speech.py
│   │   └── tkinter_gui_controller.py
│   ├── core/               # Business logic
│   │   ├── ports.py        # Abstract interfaces
│   │   ├── speech_controller.py
│   │   ├── text_processor.py
│   │   └── constants.py
│   └── constants.py
├── tests/
│   ├── test_cli.py
│   ├── test_speech_controller.py
│   ├── test_text_processor.py
│   ├── test_pynput_hotkeys.py
│   ├── test_pyttsx3_speech.py
│   └── ...
├── CONTRIBUTING.md         # This file
├── README.md
├── LICENSE
└── pyproject.toml
```

### Key Classes

- **SpeechController** (`core/speech_controller.py`) - Main orchestrator
- **TextProcessor** (`core/text_processor.py`) - Sentence segmentation
- **PynputHotkeyController** (`adapters/pynput_hotkeys.py`) - Hotkey listener
- **TkinterFloatingController** (`adapters/tkinter_gui_controller.py`) - GUI window
- **MultiprocessPyttsx3Speech** (`adapters/pyttsx3_speech.py`) - TTS backend

## Development Tips

### Faster Development Loop

```bash
# Install in editable mode
pip install -e ".[test]"

# Run tests automatically on file change (requires pytest-watch)
pip install pytest-watch
ptw
```

### Platform-Specific Testing

You should ideally test on:

```bash
# Windows
python -m pytest

# macOS
python -m pytest

# Linux
python -m pytest
```

### Debug Logging

```bash
# Run with debug output
ttsu --log-level DEBUG

# Find specific log output
ttsu --log-level DEBUG 2>&1 | grep "Speech"
```

## Questions?

- Check open issues
- Open a discussion
- Email guzmanjps@gmail.com

## Code of Conduct

Be respectful and inclusive in all interactions.

## License

By contributing, you agree your code will be licensed under MIT License.

---

**Your contributions make tts_util more accessible!** 🙏
