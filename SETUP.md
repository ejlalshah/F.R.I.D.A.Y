# F.R.I.D.A.Y Setup & Installation Guide

## Overview

This guide walks you through setting up F.R.I.D.A.Y on your Windows, Mac, or Linux computer. The system will run in the background and activate when you say "Hello Friday".

**Time required:** 20-30 minutes  
**Cost:** Free (except Claude API which is pay-as-you-go)  
**Requirements:** Python 3.9+, microphone, speaker

## Step 1: Prerequisites

### 1.1 Install Python 3.9 or Higher

Download from https://www.python.org/downloads/

On Windows, make sure to check "Add Python to PATH" during installation.

Verify installation:
```bash
python --version  # Should show 3.9 or higher
```

### 1.2 Install Git (Optional but Recommended)

This makes cloning the repository easier. Download from https://git-scm.com/

## Step 2: Get the Code

### Option A: Clone from Repository
```bash
git clone https://github.com/yourusername/friday.git
cd friday
```

### Option B: Download as ZIP
Download from the repository and extract to a folder, then navigate to it in terminal/command prompt.

## Step 3: Create Virtual Environment

A virtual environment keeps Python dependencies isolated from your system Python.

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

You'll see `(venv)` in your terminal when activated. All subsequent commands should run with this activated.

## Step 4: Install Dependencies

This installs all required Python packages:
```bash
pip install -r requirements.txt
```

This downloads about 2-3 GB of models (Whisper, Piper voices, speaker models). It may take 5-10 minutes depending on your internet speed.

## Step 5: Configure Your API Keys

### 5.1 Get Claude API Key

1. Go to https://console.anthropic.com/account/keys
2. Click "Create Key"
3. Copy the key (starts with `sk-ant-`)

### 5.2 Create .env File

Copy the template:
```bash
cp .env.example .env
```

Open `.env` in a text editor and paste your Claude API key:
```
CLAUDE_API_KEY=sk-ant-your-actual-key-here
```

Never commit this file to version control—it contains your secret key.

## Step 6: Test Your Microphone

Run the audio test:
```bash
python scripts/test_audio.py
```

This verifies your microphone works and shows audio input levels. You should see changing numbers when you speak.

## Step 7: Download Voice Models (First Run)

The system downloads models on first use, but you can pre-download them:

```bash
python scripts/download_models.py
```

This downloads:
- Whisper (speech-to-text) — ~140 MB for 'base' model
- Piper TTS voices — ~200 MB per voice
- Speaker verification model — ~50 MB

## Step 8: Start F.R.I.D.A.Y

In your terminal with the virtual environment activated:
```bash
python -m friday.main
```

You should see output like:
```
======================================================================
  F.R.I.D.A.Y - Fully Responsive Intelligent Digital Assistant for You
======================================================================
✓ F.R.I.D.A.Y ACTIVE - Say 'Hello Friday'
```

Now speak clearly: **"Hello Friday"**

After detecting your voice, you'll see:
```
🎤 Wake word detected! Listening for command...
```

Say your command, for example: **"What time is it?"**

F.R.I.D.A.Y will respond with the answer spoken aloud.

To exit, press `Ctrl+C`.

## Step 9: Set Up Windows Autostart (Optional)

To make F.R.I.D.A.Y start automatically when your computer boots:

### Using Windows Task Scheduler

1. Press `Win+R`, type `taskschd.msc`, press Enter
2. Click "Create Basic Task" in the right panel
3. Name it "F.R.I.D.A.Y"
4. Set trigger: "At startup"
5. Set action: "Start a program"
6. Program: `C:\path\to\venv\Scripts\python.exe`
7. Arguments: `-m friday.main`
8. Check "Run whether user is logged in or not"
9. Click Finish

F.R.I.D.A.Y will now start automatically.

## Step 10: Configure Settings (Optional)

Edit `friday/config.py` to customize:

**Audio Settings**
- WAKE_WORD: Change the activation phrase
- WAKE_WORD_THRESHOLD: Higher = fewer false positives
- COMMAND_TIMEOUT_SECONDS: How long to listen after wake word

**Model Selection**
- WHISPER_MODEL: 'tiny' (fast) to 'large' (accurate)
- TTS_VOICE: Different voice options

**Brain Settings**
- SYSTEM_PROMPT: Customize F.R.I.D.A.Y's personality

## Troubleshooting

### "Microphone not detected"
- Check Windows sound settings: make sure your microphone is set as default
- Run `scripts/test_audio.py` to debug
- Try specifying AUDIO_DEVICE_ID in .env

### "Claude API error"
- Verify your API key is correct in .env
- Check you have API credit: https://console.anthropic.com/account/billing/overview
- Ensure internet connection is working

### "Whisper taking too long"
- You're using a large model. Switch to 'base' or 'small' in config.py
- If on CPU, first run takes longer as it optimizes

### "Piper not found"
- Install with: `pip install piper-tts`
- Download voices: `piper-download-voice en_US-lessac-medium`

### Wake word not detecting
- The model may need tuning. Try saying "Hello Friday" clearly and slowly
- Increase WAKE_WORD_THRESHOLD if getting false positives

### False positives (activating without wake word)
- Decrease WAKE_WORD_THRESHOLD in config.py
- Or increase the threshold value (0.5 → 0.7)

## Next Steps

Now that F.R.I.D.A.Y is running, you can:

1. **Extend with custom tools** - Add new capabilities in `friday/control/executor.py`
2. **Train speaker verification** - Run `scripts/enroll_speaker.py` for voice recognition
3. **Customize personality** - Edit SYSTEM_PROMPT in config.py
4. **Create automation scripts** - Add Python scripts that F.R.I.D.A.Y can execute

## Performance Tuning

**CPU Usage**
- Wake word detection: ~2-5% when idle
- Speech processing: spikes to 30-50% during transcription
- Brain processing: depends on response complexity

**Memory Usage**
- Typical: 200-400 MB
- Whisper model loaded: +500 MB
- Multiple models loaded: +1-2 GB

If running on older hardware, use 'tiny' Whisper model and smaller voices.

## Security & Privacy

F.R.I.D.A.Y is fully local—no audio is sent to external services except:
- Claude API for text processing (required)
- Web search results (if you ask F.R.I.D.A.Y to search)

Your microphone audio never leaves your computer. The system validates all commands before executing them (see `friday/control/sandbox.py`).

## Getting Help

1. Check the troubleshooting section above
2. Enable DEBUG_MODE in .env for verbose logging
3. Check logs in the `logs/` folder
4. Review the architecture documentation in `docs/architecture.md`

## Next: Explore the Codebase

The system is modular—each component is independent:

- `audio/listener.py` - Microphone capture
- `wake_word/detector.py` - "Hello Friday" detection
- `speech/stt.py` - Audio to text
- `brain/processor.py` - Intent understanding and task planning
- `control/executor.py` - Safe command execution
- `output/speaker.py` - Text to speech

Start with `event_loop.py` to understand how they all connect.

