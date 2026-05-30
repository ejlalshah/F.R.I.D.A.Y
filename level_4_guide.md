# F.R.I.D.A.Y Level 4: AI Companion Implementation Guide

## What You're Building

Level 4 is the leap from "command executor" to "AI companion." The difference is profound. In Level 3, you said "open chrome" and the system opened chrome. In Level 4, you say "I'm tired" and the system understands you've been working for hours, suggests a break, offers to play relaxing music, and generally acts like someone who cares about your wellbeing.

This works because of three new systems:

**Conversation Memory** stores everything you've said and learns patterns. It builds a model of your preferences, habits, emotional state, and goals.

**Intelligence Layer** uses Claude API to genuinely understand context and intent. When you say "I'm tired," Claude recognizes this as emotional context, not a command. It can then make proactive suggestions.

**Voice Response** makes F.R.I.D.A.Y speak back to you instead of just printing text. This transforms it from feeling like a command-line tool to feeling like a conversation with an actual assistant.

## Installation & Setup

### Step 1: Install Required Libraries

```bash
pip install pyttsx3 --break-system-packages
```

That's the only new dependency. You already have everything else installed from previous levels.

Note: `pyttsx3` is a text-to-speech engine that works offline. Unlike cloud-based TTS services, it doesn't require internet and won't have latency issues.

### Step 2: Copy the Level 4 Files

Copy these four files into your Friday project folder (your friday/ directory):

```
level_4_memory.py       → friday/core/memory.py
level_4_intelligence.py → friday/intelligence/brain.py
level_4_voice.py        → friday/output/voice.py
level_4_event_loop.py   → main_level_4.py (in root of project)
```

### Step 3: Update Your Config

Add these settings to `friday/config.py`:

```python
# Level 4 Configuration
MEMORY_FILE = "friday_long_term_memory.json"
MAX_CONTEXT_MESSAGES = 50
VOICE_ENABLED = True
VOICE_RATE = 150  # Speech speed (100-200)
VOICE_VOLUME = 0.8  # 0.0-1.0
```

### Step 4: Test Level 4

Run it:

```bash
python main_level_4.py
```

You should see:

```
======================================================================
INITIALIZING F.R.I.D.A.Y LEVEL 4 - AI COMPANION
======================================================================

[INIT] Creating memory system...
[INIT] ✓ Memory initialized
[INIT] Creating intelligence layer...
[INIT] ✓ Intelligence system initialized
[INIT] Creating voice system...
[INIT] ✓ Voice system initialized
[INIT] Creating audio listener...
[INIT] ✓ Audio listener initialized
...
```

## How to Use F.R.I.D.A.Y Level 4

### Basic Interaction

Say "Friday" to wake up the system. Then speak naturally. F.R.I.D.A.Y will:

1. **Listen** to what you say
2. **Understand** what you actually mean (not just keywords)
3. **Remember** everything you've told it
4. **Respond** intelligently based on full context
5. **Speak** the response aloud
6. **Act** on suggestions (open apps, play music, etc)

### Example Conversations

**You:** "Friday, I'm really tired"

**F.R.I.D.A.Y:** "You've been working for 6 hours. Your energy is pretty low right now. Want me to play something relaxing, or would a quick break help you more?"

---

**You:** "Friday, what have I been asking for a lot today?"

**F.R.I.D.A.Y:** "You've opened Chrome three times and asked about your calendar twice. Looks like you're doing research and time management today. Anything specific you need help with?"

---

**You:** "Friday, I'm bored"

**F.R.I.D.A.Y:** "Let me suggest something. You usually enjoy learning new things. Want me to open a website about machine learning, or would you prefer something more recreational like music or a game?"

## Understanding the Architecture

### The Memory System (ConversationMemory)

This component does two things. First, it maintains a conversation history, which is the recent messages that Claude uses for context. Second, it builds a user model by analyzing patterns in what you say and do.

When you say "I played guitar for 2 hours," the memory system extracts that information and stores it. When you say "I'm tired after working," it updates your current emotional state. Over time, this builds a complete picture of who you are and what you like.

The memory system persists to disk (in `friday_long_term_memory.json`), so F.R.I.D.A.Y remembers you across sessions. If you use it tomorrow, it will remember that you like relaxing music in the evening or that you always open Chrome at 9 AM.

### The Intelligence Layer (IntelligenceLayer)

This is where Claude comes in. Instead of hardcoded if-else statements, you use Claude's reasoning capability to understand context and generate appropriate responses.

When you say something, the intelligence layer does three things. It analyzes your intent (is this a command, a question, or are you expressing an emotion?). It generates a contextual response using Claude with your full conversation history and user profile. It identifies any suggested actions (should I play music? suggest a break? open a browser?).

The system prompt (inside the intelligence layer) defines who F.R.I.D.A.Y is. It says things like "You're proactive—if the user seems tired, suggest something." This personality stays consistent across all interactions.

### The Voice System (VoiceResponder)

F.R.I.D.A.Y now speaks back to you instead of just printing text. The voice system uses pyttsx3, which is an offline text-to-speech engine. It runs in a background thread so it doesn't block the main event loop. If F.R.I.D.A.Y is speaking while you're talking, the system handles it gracefully.

The voice system can also play notification sounds. A "ding" when F.R.I.D.A.Y is listening, a "boop" when it's thinking, and a "chime" when it's done. These audio cues provide feedback so you know the system heard you.

### The Event Loop (Level4EventLoop)

This brings everything together. The flow is: listen for wake word → capture command → analyze intent → generate response → speak response → execute actions.

The key difference from Level 3 is that every step involves context. You're not just matching keywords. You're understanding intent, remembering history, and making intelligent decisions.

## Key Features

### 1. Emotional Context Understanding

When you say something like "I'm tired," the system doesn't just log the text. It:

Recognizes this as expressing an emotional state, not a command. Updates your user model with your current mood. Considers what might help (rest vs. music vs. productivity). Generates a response that addresses both the stated need and the underlying context.

### 2. Proactive Assistance

Instead of waiting for commands, F.R.I.D.A.Y can suggest helpful things based on context.

If you've been working for 6 hours without a break, it suggests rest. If you're bored, it suggests based on your interests. If you're stressed, it offers calming options. This feels more like having an assistant who cares about your wellbeing.

### 3. Conversation Memory

The system remembers everything you've told it. Not just in this session, but across days. If you mention your favorite music on Monday, Friday will remember it on Friday and suggest it when you seem sad.

This memory includes patterns too. If Friday notices you always open Chrome at 9 AM and check your calendar at 10 AM, it learns your routine and can proactively remind you about it.

### 4. Natural Language Conversations

Because responses are generated by Claude, not hardcoded, they feel natural and conversational. You're not getting scripted responses. You're getting thoughtful replies from an intelligent system that understands context.

## Configuration & Customization

### Adjusting Voice

The voice uses two parameters: rate (speed) and volume.

```python
# In level_4_voice.py
voicer = VoiceResponder(rate=150, volume=0.8)
```

Rate ranges from 100 (very slow) to 200 (very fast). 150 is natural speech speed. Increase it if you want faster responses, decrease it if you want slower, clearer speech.

Volume ranges from 0.0 (silent) to 1.0 (maximum). Set it lower if the voice is too loud.

### Customizing Personality

The personality is defined in the system prompt inside `IntelligenceLayer._create_system_prompt()`. You can modify it to change how F.R.I.D.A.Y behaves.

For example, if you want F.R.I.D.A.Y to be more formal, change:

```python
"You're proactive and casual in tone"
```

To:

```python
"You're professional and formal in your communication"
```

The system prompt defines the entire personality, so edit it to match how you want the assistant to behave.

### Memory Persistence

Conversation history is saved to disk every 10 interactions. You can change this frequency in `ConversationMemory.add_message()`:

```python
if self.interaction_count % 10 == 0:  # Save every 10 interactions
    self._save_memory()
```

Change the `10` to a different number if you want more frequent saves (lower number) or less frequent (higher number).

## Common Issues & Solutions

### Issue: F.R.I.D.A.Y isn't speaking

**Solution:** Make sure pyttsx3 is installed correctly. On Windows, it requires specific audio drivers. Try running this test:

```python
import pyttsx3
engine = pyttsx3.init()
engine.say("Test")
engine.runAndWait()
```

If you hear "Test" spoken, it's working. If not, check your system volume and audio drivers.

### Issue: Memory file is getting too large

**Solution:** The memory system keeps everything in `friday_long_term_memory.json`. If this file gets too large, you can archive old data. You could add a function to the memory system that moves messages older than 30 days to a separate "archive" file.

### Issue: Voice responses are delayed

**Solution:** Voice runs in a background thread, so it shouldn't block the main loop. But if you hear lag, you could adjust the event loop to capture the next user input while still speaking the previous response. The current code waits for speech to finish before listening again.

## What's Next (Level 5+)

After Level 4, the natural next steps are:

**Better wake word detection:** Replace simple keyword matching with a proper wake word detector that recognizes when you're actually talking to F.R.I.D.A.Y vs. talking about Friday.

**Skills/Plugins system:** Make it easy to add new capabilities without modifying core code. F.R.I.D.A.Y could have plugins for weather, calendar, email, smart home, etc.

**Continuous listening:** F.R.I.D.A.Y could stay "on" and respond to you without wake word in certain contexts (like if you're already in a conversation).

**Multi-turn interactions:** Support complex conversations where F.R.I.D.A.Y asks clarifying questions and builds understanding over multiple exchanges.

**Learning from feedback:** When F.R.I.D.A.Y makes a suggestion and you accept or reject it, learn from that feedback to improve future suggestions.

## Testing Your Setup

Once you have Level 4 running, here's a good test sequence:

1. Say "Friday, I'm tired" - should recognize emotional state and suggest rest
2. Say "Friday, remember that I like jazz music" - should add this to user model
3. Wait a few interactions, then say "What kind of music do I like?" - should remember jazz
4. Say "Friday, what have I been doing?" - should summarize your conversation history
5. Say "Friday, open Chrome" - should execute the command and speak confirmation

If all of these work, you have a fully functional Level 4 AI Companion.

## Architecture Diagram

```
User speaks
    ↓
Audio Listener (capture)
    ↓
Speech-to-Text (transcribe)
    ↓
Memory System (store + analyze)
    ↓
Intelligence Layer (Claude reasoning)
    ↓
Response Generated
    ↓
Voice Responder (speak aloud)
    ↓
Executor (if action needed)
    ↓
F.R.I.D.A.Y acts
```

Each component is modular and can be improved independently. You can upgrade the voice quality, switch out the TTS engine, change the LLM from Claude to something else, etc.

The key insight is that this architecture separates concerns cleanly. The voice system doesn't know about memory. The memory system doesn't know about voice. The intelligence layer is separate from both. This modularity makes the system maintainable and extensible.