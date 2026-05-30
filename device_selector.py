"""
AUDIO DEVICE SELECTOR (FIXED VERSION)
Properly tests input devices and selects best working microphone.
"""

import sounddevice as sd
import numpy as np

print("\n" + "="*70)
print("AUDIO DEVICE SELECTOR TEST (FIXED)")
print("="*70)

devices = sd.query_devices()

input_devices = [
    (i, d) for i, d in enumerate(devices)
    if d["max_input_channels"] > 0
]

print(f"\nFound {len(input_devices)} input devices:\n")

for i, d in input_devices:
    print(f"[Device {i}] {d['name']} | SR: {d['default_samplerate']}")

print("\n" + "="*70)
print("Testing devices...\n")

DURATION = 4

best_device = None
best_score = 0
best_rate = 16000

for device_id, device in input_devices:

    try:
        sr = int(device["default_samplerate"])

        print(f"\n[Device {device_id}] {device['name']}")
        print(f"Recording {DURATION}s at {sr} Hz... SPEAK NOW!")

        audio = sd.rec(
            int(DURATION * sr),
            samplerate=sr,
            channels=1,
            dtype="float32",
            device=device_id
        )
        sd.wait()

        # CLEAN signal analysis
        amplitude = np.mean(np.abs(audio))
        peak = np.max(np.abs(audio))

        print(f"Avg: {amplitude:.6f} | Peak: {peak:.6f}")

        # scoring system (better than raw amplitude)
        score = amplitude + (peak * 0.5)

        if score > best_score and amplitude > 0.001:
            best_score = score
            best_device = device_id
            best_rate = sr

        if amplitude < 0.001:
            print("→ SILENT")
        elif amplitude < 0.01:
            print("→ weak signal")
        else:
            print("→ GOOD SIGNAL")

    except Exception as e:
        print(f"✗ Error: {e}")

print("\n" + "="*70)

if best_device is not None:

    best_name = devices[best_device]["name"]

    print(f"\n✓ BEST DEVICE FOUND:")
    print(f"  Device ID: {best_device}")
    print(f"  Name: {best_name}")
    print(f"  Sample Rate: {best_rate}")
    print(f"  Score: {best_score:.6f}")

    print("\n👉 USE THIS IN listener.py:")
    print(f"""
device={best_device},
samplerate={best_rate},
""")

else:
    print("\n✗ No valid microphone detected.")

print("\n" + "="*70 + "\n")
