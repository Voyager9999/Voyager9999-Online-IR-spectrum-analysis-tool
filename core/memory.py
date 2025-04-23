import json

def load_memory(path='data/memory.json'):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return []

def save_memory(data, path='data/memory.json'):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
