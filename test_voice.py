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
