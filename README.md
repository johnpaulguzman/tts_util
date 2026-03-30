# tts_util

> A global hotkey-driven text-to-speech macro utility for accessibility and productivity.

tts_util is a lightweight, cross-platform TTS macro service that converts selected text to speech via global hotkeys. It's designed for accessibility, productivity automation, and accessibility features with minimal latency.

![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-8%20passing-brightgreen)](tests/)
[![Coverage](https://img.shields.io/badge/Coverage-80%25-brightgreen)](#testing)

## Features

- 🎤 **Global Hotkey Control** - Speak selected/copied text from anywhere
- ⚡ **Fast & Responsive** - Multiprocess architecture for non-blocking speech
- 🔧 **Flexible Text Processing** - Automatic sentence segmentation and pattern replacement
- 🌐 **Cross-Platform** - Works on Windows, macOS, and Linux
- 🎯 **Accessibility-First** - Designed for accessibility and productivity workflows

## Requirements

- **Python 3.9+**
- **pynput** - For global hotkey monitoring
- **pyttsx3** - Text-to-speech synthesis
- **pysbd** - Sentence boundary detection
- **pyperclip** - Clipboard integration

## Installation

### Quick Install

```bash
pip install git+https://github.com/johnpaulguzman/tts_util.git
```

### From Source

```bash
git clone https://github.com/johnpaulguzman/tts_util.git
cd tts_util
pip install .
```

### Development Setup (with testing)

```bash
pip install -e ".[test]"
pytest  # Verify installation
```

## Quick Start

Start the TTS service with global hotkeys:

```bash
ttsu
```

Set logging level:

```bash
ttsu --log-level DEBUG
```

## Usage

After running `ttsu`, use these hotkeys from anywhere:

- **;+[** - Start speaking selected/clipboard text
- **;+]** - Stop speaking
- **;+'** - Speak current sentence
- **;+.** - Speak next sentence
- **;+,** - Speak previous sentence
- **;+p** - Increase speech rate
- **;+o** - Decrease speech rate
- **;+q** - Stop service

### Example Workflows

**Reading Email Aloud**

```bash
# Select email text in Gmail
# Press ;+[
# tts_util reads it aloud while you continue working
```

## Architecture

tts_util uses a **ports and adapters** pattern:

```
┌──────────────────────────────────────┐
│   Controller Layer                   │
│  (Hotkeys or GUI trigger)            │
└───────────────┬──────────────────────┘
                │
┌───────────────▼──────────────────────┐
│   Speech Controller                  │
│  (Orchestrates pipeline)             │
└───────────────┬──────────────────────┘
                │
        ┌───────┴────────┬──────────────┐
        │                │              │
┌───────▼────────┐  ┌────▼────────┐  ┌─▼──────────────┐
│  Text Source   │  │Text Processor│  │Speech Adapter  │
│  (Clipboard/   │  │(Segmentation) │  │ (pyttsx3)     │
│   Selection)   │  │             │  │(Multiprocess)  │
└────────────────┘  └─────────────┘  └────────────────┘
```

- **Controllers** - Hotkey listeners or GUI windows
- **Text Source** - Extracts text from clipboard/selection
- **Text Processor** - Sentence segmentation, pattern replacement
- **Speech** - pyttsx3-based synthesis in separate process

## CLI Reference

```
ttsu [--log-level LEVEL] [up|start]

Options:
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set logging verbosity (default: INFO)
  up, start             Start the service (default command)
```

## Configuration

Text replacements and sentence processing are configurable in:

```
src/tts_util/core/constants.py
```

Modify `TEXT_REPLACEMENTS` to customize:

- Abbreviation expansions (e.g., "Dr." → "Doctor")
- Symbol replacements (e.g., "→" → "arrow")

## Testing

Run all tests:

```bash
pytest
```

Run with coverage report:

```bash
pytest --cov=src/tts_util --cov-report=html
# Open htmlcov/index.html
```

Run specific test file:

```bash
pytest tests/test_speech_controller.py -v
```

tts_util maintains 80% code coverage minimum.

## Development

### Project Structure

```
tts_util/
├── src/tts_util/
│   ├── adapters/          # pynput, pyttsx3, tkinter implementations
│   ├── core/              # Ports and business logic
│   ├── cli.py             # Command-line interface
│   └── macro_util.py      # Service composition
├── tests/                 # Full test suite
├── pyproject.toml         # Project metadata
└── README.md
```

### Running Tests

```bash
# Run all tests with verbose output
pytest -v

# Run specific test
pytest tests/test_speech_controller.py::test_speak -v

# Run with coverage
pytest --cov=src/tts_util
```

### Code Quality

Format code with black (if configured):

```bash
black src/tts_util tests
```

## Troubleshooting

### Hotkeys Not Working

Ensure no other application is capturing the hotkeys globally:

```bash
ttsu --log-level DEBUG
# Check for "Starting macro service" message
```

### No Audio Output

Check system volume and TTS engine:

```bash
python -c "import pyttsx3; pyttsx3.init().say('test').runAndWait()"
```

## Performance

- **Startup Time** - ~500ms (hotkey listener overhead)
- **Speech Latency** - <100ms from text to audio
- **Memory** - ~50-80MB (multiprocess speech engine)

## Contributing

Contributions welcome! Please:

1. ✅ Run tests: `pytest`
2. ✅ Maintain coverage ≥ 80%
3. ✅ Add tests for new features
4. ✅ Update documentation

## Accessibility

tts_util is designed with accessibility in mind:

- Global hotkey activation (no mouse required)
- GUI controller for users who prefer graphical interfaces
- TTS output for audio-only workflows
- Sentence-level segmentation for natural speech

## License

MIT License - See [LICENSE](LICENSE) file

## Related Projects

- [pynput](https://github.com/moses-palmer/pynput) - Global input monitoring
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) - Text-to-speech library
- [pysbd](https://github.com/nipunsadvilkar/pySBD) - Sentence segmentation
- [Accessibility Insights](https://accessibilityinsights.io/) - Testing framework
