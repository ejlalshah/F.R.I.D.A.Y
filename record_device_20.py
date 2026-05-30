"""
RECORD FROM DEVICE 20
Records 10 seconds of audio from Device 20 specifically
so we can hear exactly what the microphone is capturing.
"""

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import time

print("\n" + "="*70)
print("RECORDING FROM DEVICE 20")
print("="*70)
print("\nThis will record 10 seconds from Device 20 (Microphone 2)")
print("Speak 'Hello Friday' clearly during the recording.")
print("\nThe audio will be saved as 'device_20_recording.wav'")
print("="*70 + "\n")

SAMPLE_RATE = 16000
DURATION = 10
DEVICE = 20

print(f"Recording for {DURATION} seconds from Device {DEVICE}...")
print("SPEAK NOW!\n")

try:
    # Record directly from Device 20
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), 
                        samplerate=SAMPLE_RATE, 
                        channels=1, 
                        dtype='float32',
                        device=DEVICE)
    sd.wait()
    
    # Analyze
    amplitude = np.mean(np.abs(audio_data))
    
    print(f"\nRecording complete!")
    print(f"Total samples: {len(audio_data)}")
    print(f"Duration: {len(audio_data) / SAMPLE_RATE:.2f} seconds")
    print(f"Average amplitude: {amplitude:.6f}")
    print(f"Max amplitude: {np.max(np.abs(audio_data)):.6f}")
    
    # Save
    wavfile.write("device_20_recording.wav", SAMPLE_RATE, audio_data)
    print(f"\n✓ Saved to: device_20_recording.wav")
    print("\nNow open this WAV file and listen to it.")
    print("You should hear yourself saying 'Hello Friday'.")
    print("If it sounds distorted, unclear, or like noise instead of speech,")
    print("then we know why Whisper is failing.")
    
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*70 + "\n")