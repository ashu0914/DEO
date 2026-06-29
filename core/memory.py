import json

MEMORY_FILE = "memory.json"

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}