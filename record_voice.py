"""
VOICE RECORDING TEST
This records your speech to a WAV file so we can verify exactly what
the microphone is capturing and hear it ourselves.
"""

import numpy as np
from friday.audio.listener import get_audio_listener
import scipy.io.wavfile as wavfile
import time
import os

print("\n" + "="*70)
print("VOICE RECORDING TEST")
print("="*70)
print("\nThis will record 10 seconds of audio to a WAV file.")
print("Speak 'Hello Friday' clearly during the recording.")
print("\nThe audio will be saved as 'recorded_audio.wav' in your project folder.")
print("After the test, you can:")
print("1. Listen to the WAV file to hear what the microphone captured")
print("2. Share it with us to analyze")
print("="*70 + "\n")

# Initialize listener
listener = get_audio_listener()
listener.start()
print("Recording for 10 seconds... SPEAK NOW!\n")

# Record 10 seconds of audio
all_audio = []
for i in range(10):
    audio = listener.get_audio(1.0)
    if audio is not None and len(audio) > 0:
        all_audio.append(audio)
        print(f"[{i+1:02d}s] Recorded {len(audio)} samples, Amplitude: {np.mean(np.abs(audio)):.6f}")
    time.sleep(0.05)  # Small delay to avoid overlap

listener.stop()

# Combine all audio
if all_audio:
    combined_audio = np.concatenate(all_audio)
    
    # Save to WAV file
    output_path = "recorded_audio.wav"
    wavfile.write(output_path, 16000, combined_audio)
    
    print(f"\n✓ Recording saved to: {output_path}")
    print(f"  Total duration: {len(combined_audio) / 16000:.2f} seconds")
    print(f"  Total samples: {len(combined_audio)}")
    print(f"  Average amplitude: {np.mean(np.abs(combined_audio)):.6f}")
    print("\nYou can now:")
    print("1. Double-click the WAV file to listen to it")
    print("2. Check if you can hear yourself saying 'Hello Friday'")
    print("3. Share the file with us for analysis")
else:
    print("✗ No audio was recorded")

print()