# Level 4: Getting Started - Complete Setup & Testing Guide

## What You're Building

Level 4 transforms F.R.I.D.A.Y from a command executor into an AI companion. Instead of "open Chrome," you can say "I'm tired" and Friday understands, checks what you've been doing, remembers your preferences, and suggests something actually helpful. It learns from every conversation and gets better at understanding you over time.

## Prerequisites

Before you start, make sure you have:
- Python 3.8+ installed
- Your Friday project with Level 3 working (audio capture, STT, basic commands)
- About 30 minutes for setup
- Patience—Ollama downloads will take a few minutes

## Step 1: Install Ollama (5 minutes)

This is the only major external tool you need to install.

1. Go to https://ollama.ai
2. Download the Windows installer
3. Run it and follow the prompts
4. Once installed, open Command Prompt and run:

```bash
ollama pull mistral
```

This downloads the Mistral 7B model (~4GB). The download progress will be shown. Once complete, you'll have a capable language model running locally on your machine.

Keep the Command Prompt window open after this—you'll need to start the Ollama service from here.

## Step 2: Install Python Dependencies (2 minutes)

```bash
pip install requests --break-system-packages
```

That's the only new library you need. Everything else you should already have from Level 3.

Verify it's installed:

```bash
python -c "import requests; print('requests installed')"
```

## Step 3: Copy Level 4 Files into Your Project (5 minutes)

You need to add three new files to your Friday project:

**1. Copy `friday_core_memory.py` to `friday/core/memory.py`**

This is the conversation memory system. It stores everything you say, learns your patterns, and builds a model of who you are.

**2. Copy `friday_brain_intelligence_ollama.py` to `friday/brain/intelligence.py`**

This is the intelligence engine. It uses Ollama to understand your intent and generate contextual responses.

**3. Copy `friday_output_voice.py` to `friday/output/voice.py`**

This is the voice response system. Friday uses this to speak back to you instead of just printing text.

**4. Copy `level_4_event_loop_final.py` to `friday/event_loop_level_4.py`**

This is the main orchestrator that brings all the pieces together.

After copying, your project structure should look like:

```
friday/
├── core/
│   ├── event_bus.py
│   ├── types.py
│   └── memory.py                    ← NEW
├── brain/
│   ├── router.py
│   └── intelligence.py               ← NEW (Ollama version)
├── output/
│   └── voice.py                      ← NEW
├── audio/
│   └── listener.py
├── speech/
│   └── stt.py
└── event_loop_level_4.py             ← NEW
```

## Step 4: Start Ollama Service (1 minute)

Open a new Command Prompt window (don't close your previous one) and run:

```bash
ollama serve
```

You should see output like:

```
2025-04-21 14:32:15.123456 api/routes.go:123: listening on 127.0.0.1:11434
```

This means Ollama is running and ready to accept requests. **Keep this window open**—if you close it, Ollama stops and Friday won't work.

## Step 5: Test Individual Components (10 minutes)

Before running the full system, test each component to make sure everything works.

### Test 5A: Memory System

Create `test_level_4_memory.py`:

```python
from friday.core.memory import ConversationMemory

print("\nTesting Memory System...")

memory = ConversationMemory()
memory.add_message("user", "I really like jazz music")
memory.add_message("assistant", "Got it!")
memory.add_message("user", "I've been working for 6 hours")

print(f"✓ Memory initialized")
print(f"✓ Added 3 messages")
print(f"✓ Session duration: {memory.get_session_duration()}")
print(f"\nUser Profile:\n{memory.get_user_summary()}")
print("\n✓ Memory system working!\n")
```

Run it:

```bash
python test_level_4_memory.py
```

Expected output: You should see your user profile being built from the messages you added.

### Test 5B: Ollama Connection

Create `test_ollama_connection.py`:

```python
import requests

print("\nTesting Ollama Connection...")

try:
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    if response.status_code == 200:
        models = response.json().get("models", [])
        print(f"✓ Ollama is running")
        print(f"✓ Available models: {[m.get('name') for m in models]}")
    else:
        print(f"✗ Ollama error: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("✗ Cannot connect to Ollama")
    print("  Make sure 'ollama serve' is running in another window")

print()
```

Run it:

```bash
python test_ollama_connection.py
```

Expected output: Should show that Ollama is running and the Mistral model is available.

### Test 5C: Intelligence Engine

Create `test_intelligence.py`:

```python
from friday.brain.intelligence import OllamaIntelligenceEngine

print("\nTesting Intelligence Engine...")

intelligence = OllamaIntelligenceEngine()

# Test intent analysis
print("Testing intent analysis...")
intent = intelligence.understand_intent("I'm really tired")
print(f"✓ Intent: {intent['primary_intent']}")
print(f"✓ Confidence: {intent['confidence']}")
print(f"✓ Meaning: {intent['actual_meaning']}")

# Test response generation
print("\nTesting response generation...")
response = intelligence.generate_response(
    user_input="I'm bored",
    conversation_history=[],
    user_profile="New user",
    session_duration=None
)
print(f"✓ Response: {response['response'][:100]}...")

print("\n✓ Intelligence engine working!\n")
```

Run it:

```bash
python test_intelligence.py
```

Expected output: Should show that the intelligence engine successfully analyzed intent and generated a response using Ollama.

### Test 5D: Voice System

Create `test_voice.py`:

```python
from friday.output.voice import VoiceOutput
import time

print("\nTesting Voice System...")

voice = VoiceOutput()

print("Testing sounds...")
voice.play_notification('listening')
time.sleep(0.2)
print("✓ Listening sound played")

print("\nTesting speech...")
voice.speak_and_wait("Level 4 voice system is working")
print("✓ Speech complete")

print("\n✓ Voice system working!\n")
```

Run it:

```bash
python test_voice.py
```

Expected output: Your computer should make sounds and speak the test message.

## Step 6: Run the Full Level 4 System (Testing)

Once all individual tests pass, run the complete Level 4 event loop:

```bash
python friday/event_loop_level_4.py
```

You should see:

```
================================================================================
🤖 F.R.I.D.A.Y LEVEL 4: INTELLIGENCE LAYER INITIALIZATION
================================================================================

[INIT] Creating Conversation Memory...
[INIT] ✓ Memory system online
[INIT] Initializing Intelligence Engine (Ollama)...
[INIT] ✓ Intelligence engine online
[INIT] Initializing Voice System...
[INIT] ✓ Voice system online
[INIT] Initializing Audio Listener...
[INIT] ✓ Audio listener online
[INIT] Initializing Speech-to-Text...
[INIT] ✓ Speech-to-Text online
[INIT] Initializing Wake Word Detector...
[INIT] ✓ Wake word detector online
[INIT] Initializing Command Executor...
[INIT] ✓ Executor online
[INIT] Initializing Event Bus...
[INIT] ✓ Event bus online

================================================================================
✓ F.R.I.D.A.Y LEVEL 4 READY
================================================================================

================================================================================
🎙️  F.R.I.D.A.Y IS LISTENING
================================================================================

Say 'Friday' to wake me up, then speak naturally.
[SYSTEM] Starting audio listener...
[SYSTEM] ✓ Listening for wake word...
```

## Step 7: Test Conversations (Interactive)

Once F.R.I.D.A.Y is running and listening, try these conversations:

**Test 1: Simple expression**
- Say: "Friday, I'm tired"
- Expected: Friday understands you're expressing fatigue and responds with something thoughtful about your energy level

**Test 2: Memory learning**
- Say: "Friday, I really like jazz music"
- Wait a few interactions
- Say: "Friday, what kind of music do I like?"
- Expected: Friday should remember and mention jazz

**Test 3: Context awareness**
- Say: "Friday, I've been working for 5 hours"
- Say: "Friday, what should I do?"
- Expected: Friday should understand you've been working long and suggest a break or rest

**Test 4: Command execution**
- Say: "Friday, open Chrome"
- Expected: Chrome opens AND Friday acknowledges it

**Test 5: Proactive help**
- Say: "Friday, I'm bored"
- Expected: Friday doesn't just acknowledge—it suggests something based on what it knows about you

## Troubleshooting

### "Cannot connect to Ollama"

Make sure the Ollama service is running. In a separate Command Prompt window, run:

```bash
ollama serve
```

Keep this window open while using F.R.I.D.A.Y.

### "Model not found"

Run:

```bash
ollama pull mistral
```

### Responses are very slow (10+ seconds)

This is normal for the first run or on older hardware. Subsequent responses should be faster as the model warms up. If you want faster responses, you can switch to a smaller model:

```bash
ollama pull neural-chat
```

Then in your code, change `model_name="mistral"` to `model_name="neural-chat"`.

### No voice output

Check your system volume. Make sure speakers are enabled. If you don't hear anything, your TTS might not be working—try installing pyttsx3 again:

```bash
pip uninstall pyttsx3 --break-system-packages
pip install pyttsx3 --break-system-packages
```

### Friday doesn't understand me

Make sure you're speaking clearly. The microphone should be at a normal distance (not too close, not too far). If audio capture is working (from Level 3 testing), then it's either a Whisper issue or an Ollama understanding issue. Try the same phrase with the diagnostic tools to see what's being transcribed.

## What's Working Now

At this point, you have:
✓ **Conversation Memory** - Friday remembers everything you say
✓ **Intent Recognition** - Friday understands what you actually mean
✓ **Intelligent Responses** - Friday generates context-aware replies using Ollama
✓ **Voice Output** - Friday speaks back to you
✓ **Learning** - Friday's user model improves with every interaction
✓ **Continuous Listening** - Friday listens for the wake word and responds to commands

This is the foundation of an actual AI companion. Everything from Level 5 onward builds on top of this intelligence layer.

## Next: Level 5+

Once Level 4 is stable and working well, the natural next steps are:
- Level 5: **Skills/Plugins** - Make it easy to add new capabilities
- Level 6: **Deeper Context** - Multi-turn conversations with reasoning
- Level 7: **System Integration** - Calendar, email, file systems, etc.

But for now, focus on getting Level 4 solid. Let Friday learn your patterns for a few days. See what works, what doesn't, and what you'd actually want from a companion.

## Quick Checklist

Before declaring Level 4 successful:

- [ ] Ollama is installed and running (`ollama serve` in Command Prompt)
- [ ] Mistral model is downloaded (`ollama pull mistral` was successful)
- [ ] All individual component tests pass
- [ ] Full Level 4 event loop starts without errors
- [ ] Wake word detection works (say "Friday")
- [ ] Audio is captured and transcribed correctly
- [ ] Friday generates responses using Ollama
- [ ] Friday speaks responses aloud
- [ ] Memory is persistent (information from earlier in the session is remembered)
- [ ] Intent is understood (emotional expressions are recognized, not just commands)

Once all these are working, you have a functioning Level 4 AI Companion.