import json

def load_rules(path='data/rules.json'):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_rules(rules, path='data/rules.json'):
    with open(path, 'w') as f:
        json.dump(rules, f, indent=2)
