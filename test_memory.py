# test_memory.py

from friday.core.memory import ConversationMemory
import json

print("\n" + "="*70)
print("TESTING: Memory System")
print("="*70 + "\n")

# Initialize memory
print("[1] Initializing memory...")
try:
    memory = ConversationMemory(memory_file="test_memory.json")
    print("✓ Memory initialized successfully\n")
except Exception as e:
    print(f"✗ Failed to initialize memory: {e}\n")
    exit(1)

# Test adding messages
print("[2] Adding messages to memory...")
try:
    memory.add_message("user", "I really like jazz music", metadata={"type": "preference"})
    memory.add_message("assistant", "That's great! I'll remember that.")
    memory.add_message("user", "I've been working for 6 hours", metadata={"type": "context"})
    memory.add_message("assistant", "You should probably take a break soon.")
    print(f"✓ Added 4 messages. Total interactions: {memory.interaction_count}\n")
except Exception as e:
    print(f"✗ Failed to add messages: {e}\n")
    exit(1)

# Test getting context for Claude
print("[3] Getting context for Claude...")
try:
    context = memory.get_context_for_claude(include_recent_n=10)
    print(f"✓ Retrieved {len(context)} messages for Claude context")
    print(f"  Format: {json.dumps(context[0], indent=2)}\n")
except Exception as e:
    print(f"✗ Failed to get context: {e}\n")
    exit(1)

# Test user summary
print("[4] Getting user profile summary...")
try:
    summary = memory.get_user_summary()
    print("✓ User summary generated:")
    print(summary)
    print()
except Exception as e:
    print(f"✗ Failed to get user summary: {e}\n")
    exit(1)

# Test session duration
print("[5] Checking session duration...")
try:
    duration = memory.get_session_duration()
    print(f"✓ Session duration: {duration}\n")
except Exception as e:
    print(f"✗ Failed to get session duration: {e}\n")
    exit(1)

# Test memory persistence
print("[6] Testing memory persistence (saving to disk)...")
try:
    memory._save_memory()
    print("✓ Memory saved to test_memory.json\n")
except Exception as e:
    print(f"✗ Failed to save memory: {e}\n")
    exit(1)

# Test memory loading
print("[7] Testing memory loading (loading from disk)...")
try:
    memory2 = ConversationMemory(memory_file="test_memory.json")
    print(f"✓ Memory loaded. Recovered {len(memory2.all_messages)} messages")
    print(f"  First message: '{memory2.all_messages[0]['content'][:50]}...'\n")
except Exception as e:
    print(f"✗ Failed to load memory: {e}\n")
    exit(1)

print("="*70)
print("✓ MEMORY SYSTEM: ALL TESTS PASSED")
print("="*70 + "\n")