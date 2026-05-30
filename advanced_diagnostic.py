"""
ADVANCED DIAGNOSTIC: AMPLITUDE + TRANSCRIPTION
This shows both amplitude values AND what Whisper transcribes.
This will reveal if Whisper is working correctly.
"""

import numpy as np
from friday.audio.listener import get_audio_listener
from friday.speech.stt import SpeechToText
import time

print("\n" + "="*70)
print("ADVANCED DIAGNOSTIC: AMPLITUDE + TRANSCRIPTION")
print("="*70)
print("\nThis will show you:")
print("1. Real-time amplitude measurements")
print("2. When the system detects speech loud enough to transcribe")
print("3. What Whisper actually transcribes")
print("\nWhen amplitude > 0.02, the system will transcribe that audio.")
print("You will then see what Whisper heard.")
print("\nSpeak 'Hello Friday' clearly:")
print("="*70 + "\n")

# Initialize components
listener = get_audio_listener()
stt = SpeechToText()

print("Starting audio listener...")
listener.start()
print("✓ Listening... (speak now!)\n")

try:
    for i in range(60):  # Run for 60 seconds
        # Get 1 second of audio
        audio = listener.get_audio(1.0)
        
        if audio is None or len(audio) == 0:
            print(f"[{i:02d}s] ERROR: No audio data")
            time.sleep(1)
            continue
        
        # Calculate amplitude
        amplitude = np.mean(np.abs(audio))
        
        # Determine status
        if amplitude < 0.005:
            status = "SILENT"
        elif amplitude < 0.02:
            status = "quiet"
        elif amplitude < 0.05:
            status = "SPEAKING"
        else:
            status = "LOUD"
        
        # Print amplitude
        print(f"[{i:02d}s] Amplitude: {amplitude:.6f}  ({status})", end="")
        
        # If loud enough, transcribe it
        if amplitude >= 0.02:
            print(" → TRANSCRIBING...", end="", flush=True)
            try:
                # Send to Whisper
                transcription = stt.transcribe(audio)
                
                if transcription:
                    print(f"\n         ✓ Heard: '{transcription}'")
                else:
                    print(f"\n         ✗ Whisper returned empty string")
            except Exception as e:
                print(f"\n         ✗ Transcription error: {e}")
        else:
            print()  # Just newline if not transcribing
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\n\n✓ Test stopped")
finally:
    listener.stop()
    print("Audio listener stopped\n")