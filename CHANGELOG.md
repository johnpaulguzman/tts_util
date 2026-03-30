# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.1.0] - 2024-03-30

### Added

- Initial release with global hotkey and GUI-based TTS
- Floating GUI controller for text input and playback control
- Global hotkey listener (Ctrl+Shift+S to speak, Ctrl+Shift+P to stop)
- Automatic sentence segmentation for natural speech
- Clipboard integration with selected text capture
- Multiprocess architecture for non-blocking speech synthesis
- Full test suite (8 tests, 80% coverage)
- Cross-platform support (Windows, macOS, Linux)

### Features

- `ttsu` or `ttsu up` - Start hotkey-based TTS service
- `ttsu --gui` - Start with floating GUI controller
- `--log-level` - Configure logging verbosity
- Automatic text replacements (abbreviations, symbols)
- Real-time TTS with pyttsx3 backend

[Unreleased]: https://github.com/johnpaulguzman/tts-util/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/johnpaulguzman/tts-util/releases/tag/v0.1.0
