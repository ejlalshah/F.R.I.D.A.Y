# F.R.I.D.A.Y Quick Reference Guide

## Getting Started (TL;DR)

If you just want to get it running quickly:

```bash
# 1. Clone and navigate
git clone <repo-url>
cd friday

# 2. Setup environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Get Claude API key from https://console.anthropic.com/account/keys

# 5. Create .env file
cp .env.example .env
# Edit .env and add your Claude API key

# 6. Start the system
python -m friday.main

# 7. Say "Hello Friday" when you hear "Ready for next command"
```

You're done. The system is running. Say "Hello Friday" and give a command.

## Voice Commands Examples

After activation with "Hello Friday", you can say:

**Time & Information**
- "What time is it?"
- "What's the weather?"
- "Tell me about Python"

**Application Control**
- "Open Chrome"
- "Launch Notepad"
- "Open Spotify"

**Web Searching**
- "Search for AI news"
- "Look up Python tutorials"
- "Find information about quantum computing"

**Complex Tasks**
- "Open Chrome and search for artificial intelligence"
- "What's the time and weather today?"
- "Tell me a joke"

**Conversational**
- "Hello"
- "Thank you"
- "How are you?"

## Configuration Quick Reference

Edit `friday/config.py` to customize:

**To Make the Wake Word More Sensitive (fewer false negatives):**
```python
WAKE_WORD_THRESHOLD = 0.3  # Default 0.5, lower = more sensitive
```

**To Reduce False Activations (fewer false positives):**
```python
WAKE_WORD_THRESHOLD = 0.7  # Higher = more conservative
```

**To Make Transcription Faster:**
```python
WHISPER_MODEL = "tiny"  # Options: tiny, base, small, medium, large
```

**To Improve Transcription Accuracy:**
```python
WHISPER_MODEL = "small"  # Slower but more accurate
```

**To Change the Activation Phrase:**
```python
WAKE_WORD = "hey computer"  # You'll need to download the right model
```

**To Adjust How Long F.R.I.D.A.Y Listens After Wake Word:**
```python
COMMAND_TIMEOUT_SECONDS = 15  # Default 10 seconds
```

**To Use a Different Voice:**
```python
TTS_VOICE = "en_US-hfc_female-medium"  # Female voice instead of default
```

## Command Reference

**Starting the System**
```bash
python -m friday.main                    # Normal startup
DEBUG_MODE=true python -m friday.main    # With detailed logging
```

**Testing**
```bash
python scripts/test_audio.py             # Test your microphone
python scripts/enroll_speaker.py          # Train voice recognition
python scripts/download_models.py         # Pre-download models
```

**Development**
```bash
pytest                                    # Run tests
python -m friday.brain.processor          # Test just the brain
pytest tests/test_wake_word.py -v        # Test wake word detection
```

## Extending F.R.I.D.A.Y

### Adding a New Application

1. Open `friday/config.py`
2. Find `ALLOWED_APPLICATIONS` dictionary
3. Add your app:
   ```python
   ALLOWED_APPLICATIONS = {
       ...existing apps...,
       "my_app": "C:\\path\\to\\my_app.exe",
   }
   ```
4. Now you can say "Open my_app"

### Adding a New Command

The easiest way is to have Claude call a Python script. Here's how:

1. Create a script in `scripts/` directory, e.g., `my_command.py`:
   ```python
   #!/usr/bin/env python3
   import sys
   
   print("Hello from my_command!")
   ```

2. Now in your command, you can ask Claude:
   "Execute my_command script"
   
   Claude will run it and read the output to you.

### Adding a New Tool

If you want Claude to use a completely new tool (like controlling smart lights):

1. Add the tool definition in `friday/brain/processor.py`:
   ```python
   def get_tools(self):
       return [
           ...existing tools...,
           {
               "name": "control_lights",
               "description": "Control smart lights in your house",
               "input_schema": {
                   "type": "object",
                   "properties": {
                       "room": {"type": "string", "description": "Room name"},
                       "action": {"type": "string", "description": "on or off"}
                   },
                   "required": ["room", "action"]
               }
           }
       ]
   ```

2. Add execution logic in `friday/control/executor.py`:
   ```python
   def execute_tool(self, tool_name, tool_input):
       if tool_name == "control_lights":
           return self._control_lights(tool_input)
   
   def _control_lights(self, input_data):
       room = input_data.get('room')
       action = input_data.get('action')
       # Your light control code here
       return f"Turned {action} lights in {room}"
   ```

3. Now Claude can use this tool when you ask things like "Turn off the living room lights"

## Troubleshooting

### F.R.I.D.A.Y Won't Activate

**Check 1: Is the system running?**
You should see "Ready for next command" output

**Check 2: Are you saying the wake word clearly?**
Try saying "Hello Friday" slowly and deliberately

**Check 3: Is your microphone working?**
Run `python scripts/test_audio.py`

**Check 4: Is the threshold wrong?**
If it never activates, lower `WAKE_WORD_THRESHOLD`
If it activates too often, raise it

**Nuclear Option:** Run in debug mode to see wake word scores:
```bash
DEBUG_MODE=true python -m friday.main
```

You'll see confidence scores like `Wake confidence: 0.42`. If it shows scores less than 0.5 when you say the wake word, lower the threshold.

### Speech Recognition Not Working Well

**Check 1: Audio quality**
Run `python scripts/test_audio.py` and check if audio levels are good

**Check 2: Model too small**
`tiny` model is faster but less accurate. Try `base` or `small`

**Check 3: Microphone issues**
- Speak closer to the microphone
- Reduce background noise
- Check your microphone isn't muted

### Response Takes Too Long

**If STT (transcription) is slow:**
- You're using a large Whisper model. Switch to 'tiny' or 'base'

**If Claude is slow:**
- Check internet connection (API calls need network)
- The request might be complex (planning multi-step tasks)

**If TTS (speech generation) is slow:**
- Piper should be 1-2 seconds. If slower, check your system load

### Claude API Errors

**"Invalid API Key"**
- Check your Claude API key in `.env`
- Make sure it starts with `sk-ant-`

**"Rate Limited"**
- You're making too many requests
- Claude API has usage limits. Check your account at console.anthropic.com

**"No Internet Connection"**
- Claude requires internet. Check your connection
- Once F.R.I.D.A.Y understands your intent, it might work offline (if you use a local LLM instead)

### Windows Autostart Issues

**If F.R.I.D.A.Y doesn't start on boot:**
1. Open Task Scheduler (`Win+R` → `taskschd.msc`)
2. Find the F.R.I.D.A.Y task
3. Right-click → Edit
4. In the General tab, check "Run whether user is logged in"
5. In the Conditions tab, uncheck "Start the task only if the computer is on AC power"
6. Click OK

**If it starts but immediately closes:**
- The command path might be wrong
- Check that `python.exe` path is correct in the task
- Add error logging: modify the command to save output to a file:
  ```
  C:\path\to\python.exe -m friday.main > C:\logs\friday.log 2>&1
  ```

## Performance Tuning

**If running on old hardware:**

1. Use `tiny` Whisper model (faster, less accurate)
```python
WHISPER_MODEL = "tiny"
```

2. Use a smaller voice model:
```python
TTS_VOICE = "en_US-lessac-high"  # Smaller than medium
```

3. Reduce conversation history:
```python
CONVERSATION_HISTORY_LENGTH = 10
```

4. Disable debug mode:
```python
DEBUG_MODE = false
```

**If running on modern hardware:**

Use larger models for better quality:
```python
WHISPER_MODEL = "small"  # Better accuracy
TTS_VOICE = "en_US-lessac-medium"  # Good quality
```

## Viewing Logs

Logs are saved to `logs/` folder. Each session creates a new file.

To view real-time logs while running:
```bash
tail -f logs/friday_*.log  # On Mac/Linux
type logs\friday_*.log     # On Windows (or use Notepad)
```

For debugging a specific issue, enable DEBUG_MODE in `.env`:
```
DEBUG_MODE=true
```

This shows detailed information about what the system is doing at each step.

## Common Customizations

**Change F.R.I.D.A.Y's Personality**

Edit `SYSTEM_PROMPT` in `config.py`:
```python
SYSTEM_PROMPT = """You are F.R.I.D.A.Y, a sarcastic and witty AI assistant..."""
```

**Add Your Home Directory Paths Automatically**

In `config.py`, modify `ALLOWED_DIRECTORIES`:
```python
from pathlib import Path
home = Path.home()
ALLOWED_DIRECTORIES = [
    str(home / "Documents"),
    str(home / "Downloads"),
    str(home / "Desktop"),
]
```

**Add a Work Directory for Script Execution**

```python
ALLOWED_DIRECTORIES = [
    ...existing...,
    str(Path.home() / "my_automation_scripts"),
]
```

Then Claude can execute scripts from that directory.

## Getting Help

1. Check the main `SETUP.md` guide
2. Review `docs/ARCHITECTURE.md` to understand how things work
3. Enable `DEBUG_MODE` to see detailed system information
4. Check logs in the `logs/` folder
5. Check the source code comments—they explain the thinking behind each module

## Advanced: Using Ollama for Offline Mode

If you want to use F.R.I.D.A.Y completely offline (no Claude API), you can use Ollama:

1. Install Ollama from https://ollama.ai
2. In `config.py`, set:
   ```python
   OFFLINE_MODE = True
   ```
3. Modify `friday/brain/processor.py` to use Ollama instead of Claude

This gives you a fully local, fully offline voice assistant.

