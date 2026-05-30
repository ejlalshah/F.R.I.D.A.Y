import sounddevice as sd
import numpy as np
import json
import os

CONFIG_PATH = "friday/mic_config.json"


def test_device(device_id, duration=0.8):
    """Return average audio level from a device."""
    try:
        samplerate = 16000

        recording = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype='float32',
            device=device_id
        )
        sd.wait()

        return float(np.mean(np.abs(recording)))

    except Exception:
        return 0.0


def find_best_microphone():
    """Scan all devices and pick the best one."""
    devices = sd.query_devices()
    best_device = None
    best_score = 0

    print("\n[MIC SELECTOR] Scanning microphones...\n")

    for i, dev in enumerate(devices):
        if dev["max_input_channels"] <= 0:
            continue

        print(f"Testing [{i}] {dev['name']}")

        score = test_device(i)

        print(f"   → score: {score:.6f}")

        if score > best_score:
            best_score = score
            best_device = i

    print("\n[MIC SELECTOR] BEST DEVICE:", best_device, "score:", best_score)

    return best_device


def load_or_create_mic():
    """Load saved mic or re-detect if missing."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                return data["device"]
        except Exception:
            pass

    device = find_best_microphone()

    with open(CONFIG_PATH, "w") as f:
        json.dump({"device": device}, f)

    return device
