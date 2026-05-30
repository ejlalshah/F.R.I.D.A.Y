from friday.brain.intelligence import OllamaIntelligenceEngine

print("\nTesting Intelligence Engine...")

intelligence = OllamaIntelligenceEngine()

# Test intent analysis
print("Testing intent analysis...")
intent = intelligence.understand_intent("I'm really tired")
print(f"✓ Intent: {intent['primary_intent']}")
print(f"✓ Confidence: {intent['confidence']}")
print(f"✓ Meaning: {intent['actual_meaning']}")

# Test response generation
print("\nTesting response generation...")
response = intelligence.generate_response(
    user_input="I'm bored",
    conversation_history=[],
    user_profile="New user",
    session_duration=None
)
print(f"✓ Response: {response['response'][:100]}...")

print("\n✓ Intelligence engine working!\n")
