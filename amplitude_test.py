"""
SIMPLE AMPLITUDE TEST
This script shows you exactly what amplitude (loudness) the system is measuring
when you speak. Run this and watch the real-time amplitude values.
"""

import numpy as np
from friday.audio.listener import get_audio_listener
import time

print("\n" + "="*70)
print("SIMPLE AMPLITUDE TEST")
print("="*70)
print("\nThis will show you the amplitude (loudness) values in real-time.")
print("Speak 'Hello Friday' and watch the amplitude numbers change.")
print("\nAmplitude scale:")
print("  0.00000 - 0.00500 = SILENT (background noise)")
print("  0.00500 - 0.02000 = QUIET (system won't transcribe)")
print("  0.02000 - 0.05000 = SPEAKING (system will transcribe)")
print("  0.05000+ = LOUD")
print("\nThreshold for transcription: 0.02")
print("\nNow speak 'Hello Friday' and watch below:")
print("="*70 + "\n")

# Start the audio listener
listener = get_audio_listener()
print("Starting audio listener...")
listener.start()
print("✓ Listening... (speaking now!)\n")

try:
    for i in range(60):  # Run for 60 seconds
        # Get 1 second of audio
        audio = listener.get_audio(1.0)
        
        if audio is None or len(audio) == 0:
            print(f"[{i:02d}s] No audio data")
            time.sleep(1)
            continue
        
        # Calculate amplitude
        amplitude = np.mean(np.abs(audio))
        
        # Determine what the amplitude means
        if amplitude < 0.005:
            status = "SILENT"
            indicator = ""
        elif amplitude < 0.02:
            status = "quiet"
            indicator = ""
        elif amplitude < 0.05:
            status = "SPEAKING ✓"
            indicator = " ← SYSTEM WILL TRANSCRIBE"
        else:
            status = "LOUD"
            indicator = " ← VERY LOUD"
        
        # Print the amplitude with formatting
        print(f"[{i:02d}s] Amplitude: {amplitude:.6f}  ({status}){indicator}")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\n\n✓ Test stopped")
finally:
    listener.stop()
    print("Audio listener stopped\n")