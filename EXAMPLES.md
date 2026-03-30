# tts_util Examples

Examples and advanced usage patterns for tts_util.

## Basic Usage

### Start with Hotkeys

```bash
ttsu
# Now you can use:
# ;+[: Start speaking
# ;+]: Stop speaking
# ;+': Speak current sentence
# ;+.: Speak next sentence
# ;+,: Speak previous sentence
# ;+p: Increase rate
# ;+o: Decrease rate
# ;+q: Stop service
```

Select text anywhere and press ;+[:

```
Selected text: "The quick brown fox jumps over the lazy dog"
→ tts_util reads it aloud
```



### Set Debug Logging

```bash
ttsu --log-level DEBUG
```

Output:

```
2024-03-30 10:15:22 DEBUG tts_util.core.speech_controller: Speaking: "Hello world"
2024-03-30 10:15:22 DEBUG tts_util.core.text_processor: Segmented into 1 sentences
```

## Advanced Examples

### Reading Email Aloud

```bash
# 1. Open Gmail
# 2. Select email body
# 3. Press ;+[
# → tts_util reads email content
```



### Code Review Workflow

```bash
# 1. Open GitHub PR
# 2. Select code snippet
# 3. Press ;+[
# → tts_util reads code structure
# Listen for unclear variable names or logic
```

### Accessibility for Documentation

Enable tts_util as system-level TTS for all applications:

```bash
# Start in background (Linux/macOS)
ttsu &

# Or on Windows with task scheduler
# (Add to Startup folder)
```

Now any app can leverage your system TTS via clipboard.


## Configuration Examples

### Custom Text Replacements

Edit `src/tts_util/core/constants.py`:

```python
TEXT_REPLACEMENTS = {
    # Abbreviations
    "Dr.": "Doctor",
    "Mr.": "Mister",
    "etc.": "et cetera",

    # Symbols
    "→": "arrow",
    "←": "left arrow",
    "↑": "up arrow",
    "↓": "down arrow",
    "**": "bold",

    # Code-specific
    "def ": "define ",
    "func ": "function ",
    "async ": "asynchronous ",
}
```

Then rebuild:

```bash
pip install -e .
```

### Speed Control (Future)

Currently pyttsx3 rate can be adjusted programmatically:

```python
# In adapters/pyttsx3_speech.py
def set_rate(rate):
    """Set speech rate (100-300, default 150)"""
    engine.setProperty('rate', rate)
```

### Voice Selection (Future)

```python
# Available voices
voices = engine.getProperty('voices')
for i, voice in enumerate(voices):
    print(f"{i}: {voice.name}")

# Select voice
engine.setProperty('voice', voices[1].id)
```

## Integration Examples

### Monitor Log Files

```bash
# Read new log entries as they appear
tail -f app.log | while IFS= read -r line; do
    echo "$line" | xclip -selection clipboard
    sleep 1
    # ;+[ would be pressed by external tool
done
```

### Accessibility Macro

Create a system-wide hotkey that reads clipboard:

**Linux (using xbindkeys)**:

```bash
# ~/.xbindkeysrc
"xclip -selection clipboard -o | tts_util-read"
    Alt+Shift+t
```

**macOS (using Automator)**:

1. New Quick Action
2. Add "Run Shell Script": `pbpaste | ttsu`
3. Assign hotkey via System Preferences

**Windows (using AutoHotkey)**:

```autohotkey
#t::
{
    text := A_Clipboard
    Run, py.exe -m tts_util --speak "`%text`%"
}
```

### Text Processing Pipeline

```bash
#!/bin/bash
# Extract, process, and speak PDF text

PDF=$1
# Extract with pdftotext
pdftotext "$PDF" -

# Process and speak
| ttsu --gui
```

## Performance Tips





### Handle Long Documents

For documents longer than 1-2 pages:

```bash
# Split into chunks
# 1. Copy first section
# 2. ;+[ (speak)
# 3. ;+] (stop)
# 4. Go to next section
```

## Troubleshooting Examples

### Hotkeys Not Working

```bash
# Check listener status
ttsu --log-level DEBUG
# Look for "Starting macro service" message

# Verify hotkey isn't already bound
xbindkeys -l  # Linux
kbind -l      # macOS
AutoHotkey    # Windows
```

### No Audio

```bash
# Test system audio
speaker-test -t sine -f 1000 -l 1  # Linux
afplay /System/Library/Sounds/Glass.aiff  # macOS

# Test pyttsx3 directly
python -c "import pyttsx3; pyttsx3.init().say('test').runAndWait()"
```





## Integration with Other Tools

### Slack Integration (Future)

```bash
# Speak Slack notifications
slack-cli | while read msg; do
    echo "$msg" | xclip -selection clipboard
    # Trigger ;+[
done
```

### Email Reading

Use email client's "read aloud" and pipe to system TTS:

```bash
# Mutt integration
# Select mail→press 'm' (macro)
# Pipes message to: cat | xclip -selection clipboard
# Then press ;+[
```

### RSS Feed Reader

```bash
# Combine with RSS reader
# Select article
# Press ;+[ to read it
```

## See Also

- [tts_util README](../README.md)
- [pyttsx3 Documentation](https://pyttsx3.readthedocs.io/)
- [pynput Documentation](https://pynput.readthedocs.io/)
- [pysbd Documentation](https://github.com/nipunsadvilkar/pySBD)
