# Contributing to tts_util

Thank you for your interest in contributing! We welcome bug reports, feature requests, and pull requests.

## Getting Started

### Development Installation

```bash
git clone https://github.com/johnpaulguzman/tts_util.git
cd tts_util
pip install -e ".[test]"
```

### Run Tests

All tests must pass before submitting a PR:

```bash
pytest
```

This runs 8 tests and enforces 80% code coverage.

## Code Standards

### Style Guide

- **Formatter**: [black](https://github.com/psf/black) (if configured)
- **Linter**: [pylint](https://www.pylint.org/) (recommended)
- **Type Hints**: Encouraged for public APIs

### Testing Requirements

- Add tests for all new features
- Maintain minimum 80% code coverage
- Run tests locally: `pytest`
- Check coverage: `pytest --cov=src/tts_util --cov-report=html`

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add hotkey customization via config file
fix: handle clipboard access permission errors
docs: add GUI mode screenshot to README
refactor: unify text processing pipeline
test: add edge cases for multiline text
```

## Submission Process

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feat/my-feature`
3. **Make changes** and test locally: `pytest`
4. **Commit** with clear messages
5. **Push** to your fork
6. **Create a Pull Request** with:
   - Clear description of changes
   - Reference to any related issues
   - Evidence that tests pass

## Bug Reports

When reporting bugs, include:

- Python version: `python --version`
- Your OS (Windows/macOS/Linux)
- Command you ran and full error traceback
- Whether running in hotkey mode or GUI mode
- Steps to reproduce

## Feature Requests

Consider these questions:

- Will this benefit many users?
- Does it align with project goals (accessibility-first TTS)?
- Are there any breaking changes?
- How would this interact with existing features?

## Project Structure

Understanding the codebase:

```
src/tts_util/
├── cli.py                    # Command-line interface
├── macro_util.py             # Service composition
├── adapters/                 # Implementation adapters
│   ├── pynput_hotkeys.py    # Global hotkey listener
│   ├── pynput_text_source.py # Clipboard/selection source
│   ├── pyttsx3_speech.py    # TTS synthesis
│   └── tkinter_gui_controller.py # GUI window
├── core/                     # Business logic
│   ├── ports.py             # Abstract interfaces
│   ├── speech_controller.py # Main orchestration
│   └── text_processor.py    # Text segmentation & processing
└── constants.py              # Configuration & replacements
```

### Key Classes

- **SpeechController** - `core/speech_controller.py` - Main orchestrator
- **TextProcessor** - `core/text_processor.py` - Sentence segmentation and replacements
- **PynputHotkeyController** - `adapters/pynput_hotkeys.py` - Hotkey listener
- **TkinterFloatingController** - `adapters/tkinter_gui_controller.py` - GUI window
- **MultiprocessPyttsx3Speech** - `adapters/pyttsx3_speech.py` - Multiprocess TTS

## Areas for Contribution

### High Priority

- [ ] Configuration file support (.ttsurc, config.yaml)
- [ ] Custom hotkey binding
- [ ] Voice selection UI in GUI mode
- [ ] Speed/pitch controls

### Medium Priority

- [ ] Clipboard history integration
- [ ] Multiple language support
- [ ] Keyboard shortcuts documentation
- [ ] Performance profiling

### Low Priority

- [ ] TTS engine alternatives (Azure, Google Cloud)
- [ ] Web interface
- [ ] Plugin system
- [ ] Speech recognition (reverse direction)

## Testing Tips

### Running Specific Tests

```bash
# Single test file
pytest tests/test_text_processor.py -v

# Single test function
pytest tests/test_speech_controller.py::test_speak_empty_text -v

# With coverage
pytest --cov=src/tts_util --cov-report=term-missing
```

### Mock Testing

Since tts_util handles system-level input/output (clipboard, hotkeys, audio), use mocks:

```python
from unittest.mock import Mock, patch

def test_my_feature():
    with patch('tts_util.adapters.pynput_hotkeys.Listener'):
        # Your test here
        pass
```

## Accessibility Considerations

This project is fundamentally about accessibility. When contributing:

- Test with screen readers if possible
- Ensure keyboard-only workflows are supported
- Provide fallbacks for users without mouse/audio
- Document accessibility features

## Platform-Specific Issues

### Windows

- Tkinter usually included with Python
- Global hotkeys work reliably
- Test clipboard encoding with non-ASCII

### macOS

- May need to allow microphone/clipboard permissions
- Tkinter installation: `brew install python-tk@3.9`
- GPU support for TTS varies

### Linux

- Install tkinter: `sudo apt-get install python3-tk`
- X11/Wayland compatibility varies by distro
- Test on common distributions (Ubuntu, Fedora)

## Questions?

Feel free to:

- Open an issue for discussion
- Check existing issues for similar topics
- Add labels: `question`, `discussion`, `help-wanted`, `a11y` (accessibility)

Thank you for contributing! 🙏
