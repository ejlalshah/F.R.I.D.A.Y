# F.R.I.D.A.Y System Architecture

## Executive Summary

F.R.I.D.A.Y is a fully-local voice AI assistant that runs continuously on your personal computer. The system consumes minimal resources while idle (2-5% CPU), activates only when you say "Hello Friday", and responds intelligently to voice commands with text-to-speech output.

The architecture prioritizes responsiveness, safety, and modularity. Each component is independent and can be tested in isolation.

## System Components

### 1. Audio Listener Module (`audio/listener.py`)

**Purpose:** Continuously capture microphone input without blocking the main program.

**How it Works:**
The listener creates a background thread that uses the sounddevice library to open a stream from your microphone. Every 512 audio samples (32 milliseconds at 16kHz sample rate), it receives a callback with new audio data.

Instead of storing all audio in memory (which would consume gigabytes per hour), it uses a ring buffer—a fixed-size circular array. Imagine a tape loop: as new audio is recorded, it overwrites the oldest audio once you reach the end. This keeps memory usage constant regardless of how long the system runs.

**Key Methods:**
- `start()` - Begin capturing audio
- `get_audio(seconds)` - Retrieve the last N seconds of audio
- `stop()` - Stop capturing

**Memory Profile:** 160,000 samples × 4 bytes (float32) = 640 KB for a 10-second ring buffer.

### 2. Wake Word Detection (`wake_word/detector.py`)

**Purpose:** Detect "Hello Friday" with minimal false positives and false negatives.

**How it Works:**
The system uses openWakeWord, which bundles lightweight neural networks (ONNX format) trained specifically for wake word detection. The network runs on your CPU in 50-100 milliseconds per audio chunk.

The detector continuously checks a 2-second sliding window of audio. When it finds the wake word with confidence above a threshold (default 0.5 out of 1.0), it fires a callback that activates the full processing pipeline.

To prevent the same word from triggering multiple times, the system enforces a 1-second cooldown between detections.

**Architecture Decision:** Why local neural networks instead of cloud APIs?
- Cloud: Milliseconds of latency, privacy concerns, internet dependency
- Local: Instant response (feels reactive), offline capability, cheaper

The trade-off is slightly lower accuracy, but for a focused wake phrase like "Hello Friday", local performance is excellent.

**Alternative Options:**
- Picovoice Porcupine (faster, more accurate, costs money)
- Snowboy (deprecated but still available)
- Cloud services (Azure, Google, AWS - slower, cloud-dependent)

### 3. Speaker Verification (`speaker_verification/`)

**Purpose:** Verify that only the owner's voice can control the system.

**How it Works:**
During setup, you record 30 seconds of speech. The system extracts voice embeddings—mathematical fingerprints of your voice—using a pre-trained neural network (ECAPA-TDNN from SpeechBrain).

When someone speaks a command, the system computes their embedding and compares it to yours using cosine similarity. If the similarity score is above a threshold (default 0.75), access is granted. Otherwise, the command is rejected.

**Why This Matters:**
Without speaker verification, family members or anyone nearby could control your system. With it, F.R.I.D.A.Y is a personal assistant that responds only to you.

**Technical Details:**
Embeddings are 192-dimensional vectors in speaker space. Cosine similarity measures the angle between two vectors (values 0-1, where 1 = identical, 0 = completely different).

### 4. Speech-to-Text (`speech/stt.py`)

**Purpose:** Convert audio to text with high accuracy.

**How it Works:**
Whisper is OpenAI's speech recognition model trained on 680,000 hours of multilingual and multitask supervised data. It's robust to accents, background noise, and technical language.

The system runs the model locally on your computer. The 'base' model (140MB) strikes a good balance between accuracy and speed, transcribing 10 seconds of audio in 2-3 seconds on a modern CPU.

**Model Sizes:**
- tiny (39MB): ~1-2 seconds per 10s audio, lower accuracy
- base (140MB): ~2-3 seconds per 10s audio, good accuracy (recommended)
- small (466MB): ~3-4 seconds per 10s audio, better accuracy
- medium (466MB): ~5-8 seconds per 10s audio, higher accuracy
- large (2.9GB): ~10-15 seconds per 10s audio, best accuracy

The choice depends on your computer's specifications. On a modern laptop with GPU, 'base' or 'small' work well. On older hardware, 'tiny' provides faster responses.

### 5. Brain Module (`brain/processor.py`)

**Purpose:** Understand user intent and decide what actions to take.

**How it Works:**
The brain is where F.R.I.D.A.Y becomes intelligent. After transcribing user text, the system sends it to Claude (via the Anthropic API) along with:
- A system prompt defining F.R.I.D.A.Y's personality
- A list of available tools (open app, search web, etc.)
- Conversation history (last 20 messages)

Claude reads the user's request, understands what they want, and decides whether to:
- Answer directly: "What time is it?" → Claude computes the answer
- Use a tool: "Open Chrome" → Claude requests the open_application tool
- Take multiple steps: "Research AI companies" → Claude breaks it into search and summarize steps

This architecture is called function calling or tool use. It's powerful because Claude can reason about complex, multi-step tasks and execute them sequentially.

**Conversation Memory:**
The system remembers the last 20 conversation turns. This allows context awareness:
- User: "What's the capital of France?"
- F.R.I.D.A.Y: "Paris"
- User: "Tell me more about it"
- F.R.I.D.A.Y: Knows "it" refers to Paris, not France

Without memory, the second response would be generic. With memory, it's contextual.

### 6. System Control (`control/executor.py`)

**Purpose:** Execute system commands safely without allowing malicious operations.

**How it Works:**
Claude doesn't directly execute commands. Instead, it requests specific actions through a whitelist:
- open_application(app_name)
- search_web(query)
- get_current_time()
- execute_script(script_path)
- read_file(file_path)
- list_files(directory)

Each request goes through SandboxValidator, which checks:
- Is this application in the approved list?
- Is this file path in an allowed directory?
- Is this operation safe?

If validation fails, the request is rejected with a message explaining why.

**Example Validation Rules:**
```
ALLOWED_APPLICATIONS = {
    'chrome': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'notepad': 'notepad.exe',
}

ALLOWED_DIRECTORIES = [
    'C:\\Users\\username\\Documents',
    'C:\\Users\\username\\Desktop',
]

FORBIDDEN_DIRECTORIES = [
    'C:\\Windows',      # System files
    'C:\\Program Files\\Windows',  # System apps
    '/etc',             # Linux system config
]
```

This "fail safe" philosophy means if there's doubt, the operation is rejected.

### 7. Text-to-Speech (`output/speaker.py`)

**Purpose:** Convert response text to spoken audio and play it.

**How it Works:**
Piper TTS uses neural networks to generate natural-sounding speech. Unlike traditional text-to-speech (which sounds robotic), neural TTS captures intonation and rhythm.

Piper generates audio in 1-2 seconds for a typical response. The audio is played back through your speakers using sounddevice.

**Voice Options:**
Piper includes voices in multiple accents and genders:
- en_US-lessac-medium (recommended - natural sounding)
- en_US-hfc_female-medium (female voice)
- en_GB-* (British English)
- And many others

**Why Piper Instead of Alternatives:**
- ElevenLabs: Better quality, but cloud-based and costs money
- Google/Amazon TTS: Cloud-based, need API keys
- Festival/eSpeak: Older, sounds robotic
- Piper: Good quality, fast, fully offline, free

### 8. Event Loop (`event_loop.py`)

**Purpose:** Orchestrate all modules in a continuous state machine.

**How it Works:**
The event loop has four states, cycling continuously:

1. **IDLE:** The system listens passively for the wake word. CPU is mostly idle, consuming 2-5% of resources.

2. **ACTIVE:** When "Hello Friday" is detected, the system enters ACTIVE state and begins recording the command. It listens for up to 10 seconds or until 2 seconds of silence, whichever comes first.

3. **PROCESSING:** The system transcribes audio to text, sends it to Claude, and executes any requested tools. This is where CPU usage spikes to 30-50%.

4. **RESPONDING:** The system generates speech from Claude's response and plays it back. After finishing, the system returns to IDLE.

This state machine prevents race conditions and ensures the system is always in a well-defined state.

**Pseudo-code of the Loop:**
```
while system_running:
    audio_chunk = microphone.read()
    ring_buffer.append(audio_chunk)
    
    if wake_word_detector.is_triggered():
        command_audio = listen_for_command()
        user_text = speech_to_text(command_audio)
        response_text = brain.process(user_text)
        speaker.play(response_text)
```

## Data Flow Diagram

```
┌─────────────────┐
│   Microphone    │
└────────┬────────┘
         │ raw audio stream
         ↓
┌────────────────────────┐
│  Audio Listener        │
│  (ring buffer, 10s)    │
└────────┬───────────────┘
         │ last 2 seconds
         ↓
┌────────────────────────┐
│  Wake Word Detector    │
│  ("Hello Friday"?)     │
└────────┬───────────────┘
         │ NO → loop back
         │ YES ↓
┌────────────────────────┐
│  Speaker Verification  │
│  (your voice?)         │
└────────┬───────────────┘
         │ NO → reject
         │ YES ↓
┌────────────────────────┐
│  Command Listener      │
│  (listen until silence)│
└────────┬───────────────┘
         │ audio
         ↓
┌────────────────────────┐
│  Speech-to-Text        │
│  (Whisper)             │
└────────┬───────────────┘
         │ text
         ↓
┌────────────────────────┐
│  Brain (Claude)        │
│  (understand intent)   │
└────────┬───────────────┘
         │ decide what to do
         ↓
┌────────────────────────┐
│  System Control        │
│  (execute tools)       │
└────────┬───────────────┘
         │ results
         ↓
┌────────────────────────┐
│  Claude (reasoning)    │
│  (generate response)   │
└────────┬───────────────┘
         │ text response
         ↓
┌────────────────────────┐
│  Text-to-Speech        │
│  (Piper)               │
└────────┬───────────────┘
         │ audio
         ↓
┌────────────────────────┐
│  Speaker               │
│  (play audio)          │
└────────┬───────────────┘
         │
         ↓ (back to IDLE)
```

## Deployment Architecture

### Single Machine Deployment

F.R.I.D.A.Y runs as a background process on a single PC:

```
┌─────────────────────────────────────────────┐
│         Windows/Mac/Linux Computer          │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │    F.R.I.D.A.Y Process              │   │
│  │  ├─ Audio Thread                    │   │
│  │  ├─ Wake Word Thread                │   │
│  │  ├─ Main Event Loop Thread          │   │
│  │  └─ API Communication Thread        │   │
│  └─────────────────────────────────────┘   │
│         ↓              ↓                    │
│  ┌──────────┐  ┌──────────────┐           │
│  │Microphone│  │   Speakers   │           │
│  └──────────┘  └──────────────┘           │
│                                             │
│  [Internet] → Claude API (cloud)           │
└─────────────────────────────────────────────┘
```

## Threading Model

F.R.I.D.A.Y uses multiple threads to keep the system responsive:

**Main Thread:** Manages state transitions and orchestrates other components.

**Audio Thread:** Runs inside sounddevice, continuously capturing from microphone. This is a callback thread that runs automatically.

**Wake Word Monitor Thread:** Continuously checks the ring buffer for the wake word pattern.

**Processing Thread:** When activated, the event loop may spawn additional threads for CPU-intensive operations like model inference.

**Thread Safety:** The ring buffer uses a threading lock to prevent the audio thread and main thread from accessing the buffer simultaneously. This prevents data corruption if they're both trying to read/write at the same moment.

## Performance Characteristics

**CPU Usage:**
- Idle (listening): 2-5% (just audio capture)
- Processing (STT, inference): 30-50% (brief spikes)
- Responding (TTS): 10-20%

**Memory Usage:**
- Base: 200-300 MB
- Whisper model loaded: +500 MB
- Piper TTS loaded: +200 MB
- Total typical: 900 MB to 1.2 GB

**Latency:**
- Wake word to activation: 100-500 ms
- Speech capture (silence detection): 2-3 seconds after speaking
- STT (Whisper base): 2-3 seconds
- Brain processing: 1-5 seconds (depends on complexity)
- TTS: 1-2 seconds
- Total: 6-15 seconds from wake word to hearing response

This may seem slow compared to Alexa, which is 1-2 seconds. But remember: Alexa is a cloud service with optimized infrastructure. F.R.I.D.A.Y runs entirely locally, which naturally adds latency. The trade-off is privacy and offline capability.

## Security Model

**Principle: Never trust external input without validation.**

**Threat Model:**
1. Someone nearby says "Hello Friday" → Blocked by speaker verification
2. Remote attacker (via compromised computer) → Blocked by tool whitelist
3. Malicious Claude response → Blocked by sandbox validator
4. Accidental file deletion → Blocked by allowed directories whitelist

**Defense Layers:**
- Layer 1: Speaker verification (only your voice activates the system)
- Layer 2: Tool whitelist (Claude can only request approved actions)
- Layer 3: Directory whitelist (can only access allowed file paths)
- Layer 4: Command validation (all tool inputs are validated before execution)

**What's Not Protected Against:**
- If your Claude API key is compromised, attacker can use your quota
- If your computer is physically compromised, attacker can do anything
- If you grant permission to execute arbitrary scripts, malicious scripts can run

These are inherent to any local AI system. The key is: F.R.I.D.A.Y itself doesn't bypass these protections.

## Extensibility

**Adding New Tools:**
To let Claude use a new tool (for example, controlling smart lights):

1. Add the tool definition to `ToolDefinitions.get_tools()` in `brain/processor.py`
2. Add the execution logic to `SystemExecutor.execute_tool()` in `control/executor.py`
3. Add validation rules in `SandboxValidator` if needed

**Customizing the Brain:**
Edit the `SYSTEM_PROMPT` in `config.py` to change F.R.I.D.A.Y's personality and capabilities.

**Adding Custom Commands:**
Create Python scripts in `scripts/` directory. Claude can execute them via the `execute_script` tool.

**Changing Voice Models:**
Update `WHISPER_MODEL` and `TTS_VOICE` in `config.py` to use different models.

## Known Limitations

**Latency:** 6-15 seconds from wake word to response is slow compared to cloud services. This is the cost of local processing.

**Model Size:** Whisper requires 140MB+ to download. On slow connections, first run may take a while.

**Accuracy:** Local wake word detection is less accurate than cloud services trained on millions of hours. Expect occasional false negatives (not detecting the wake word).

**Hardware Requirements:** Requires modern CPU and 1-2GB available RAM. Very old systems may struggle.

**Single User:** Speaker verification can support multiple users but requires separate enrollment for each. The current system is optimized for one primary user.

## Future Enhancements

**Multi-user Support:** Enroll multiple family members and detect who spoke.

**Offline Brain:** Replace Claude with local LLM (Ollama, Llama 2, etc.) for completely offline operation.

**Visual Feedback:** Add LED status indicators and GUI window showing real-time transcription.

**Custom Wake Words:** Train personal wake word models instead of using pre-built ones.

**Local Search:** Integrate local search capabilities (disk, files) without needing web search.

**Voice Cloning:** Train the TTS on your voice for more personalized responses.

