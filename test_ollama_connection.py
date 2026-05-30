import requests

print("\nTesting Ollama Connection...")

try:
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    if response.status_code == 200:
        models = response.json().get("models", [])
        print(f"✓ Ollama is running")
        print(f"✓ Available models: {[m.get('name') for m in models]}")
    else:
        print(f"✗ Ollama error: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("✗ Cannot connect to Ollama")
    print("  Make sure 'ollama serve' is running in another window")

print()