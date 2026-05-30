"""
Quick script to list all audio input devices and test them
"""

import sounddevice as sd
import numpy as np

print("\n" + "="*80)
print("AUDIO DEVICE SCANNER - Finding Your Microphone")
print("="*80 + "\n")

# List all devices
print("Available Audio Devices:\n")
devices = sd.query_devices()

input_devices = []
for i, device in enumerate(devices):
    if device['max_input_channels'] > 0:
        input_devices.append((i, device))
        print(f"Device {i}: {device['name']}")
        print(f"  Input channels: {device['max_input_channels']}")
        print(f"  Sample rate: {device['default_samplerate']} Hz")
        print()

if not input_devices:
    print("❌ No input devices found!")
    exit(1)

print("\n" + "="*80)
print("TESTING DEVICES FOR AUDIO CAPTURE")
print("="*80 + "\n")

# Test each input device
for device_id, device_info in input_devices:
    print(f"\nTesting Device {device_id}: {device_info['name']}")
    print("-" * 60)
    
    try:
        # Try to record 1 second from this device
        print(f"  Recording 1 second...", end="", flush=True)
        
        recording = sd.rec(
            int(16000 * 1),  # 1 second at 16kHz
            samplerate=16000,
            channels=1,
            device=device_id,
            dtype=np.float32,
            blocksize=512
        )
        sd.wait()
        
        # Check amplitude
        amplitude = np.mean(np.abs(recording))
        print(f" Done")
        print(f"  Amplitude: {amplitude:.6f}")
        
        if amplitude > 0.01:
            print(f"  ✓ GOOD - This device is picking up audio!")
        elif amplitude > 0.001:
            print(f"  ⚠ WEAK - This device picks up audio but it's very quiet")
        else:
            print(f"  ✗ SILENT - This device is not picking up audio")
    
    except Exception as e:
        print(f" ERROR")
        print(f"  Error: {e}")

print("\n" + "="*80)
print("RECOMMENDATION")
print("="*80)
print("""
Look for a device that:
1. Has "Microphone" or "Microphone 2" in the name
2. Shows GOOD amplitude (> 0.01)
3. Successfully recorded without errors

Once you find it, note the Device number and update your listener.py:

In friday/audio/listener.py line ~170, change:
    device=20,  # OLD - no longer valid

To:
    device=X,   # Where X is the working device number
""")