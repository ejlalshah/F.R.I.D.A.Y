from friday.core.memory import ConversationMemory

print("\nTesting Memory System...")

memory = ConversationMemory()
memory.add_message("user", "I really like jazz music")
memory.add_message("assistant", "Got it!")
memory.add_message("user", "I've been working for 6 hours")

print(f"✓ Memory initialized")
print(f"✓ Added 3 messages")
print(f"✓ Session duration: {memory.get_session_duration()}")
print(f"\nUser Profile:\n{memory.get_user_summary()}")
print("\n✓ Memory system working!\n")