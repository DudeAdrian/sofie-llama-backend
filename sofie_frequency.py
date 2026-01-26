import json, random

# Load ritual map
with open("ritual_map.json", "r", encoding="utf-8") as f:
    ritual_map = json.load(f)

# Get all available frequencies
frequencies = list(ritual_map.keys())

# Suggest a random frequency and its purpose
def suggest_frequency():
    freq = random.choice(frequencies)
    purpose = ritual_map[freq]
    return f"Suggested frequency: {freq} Hz — {purpose}."

# Get a specific frequency (if user asks for one)
def get_frequency_info(hz: str):
    return f"{hz} Hz — {ritual_map.get(hz, 'Unknown purpose')}."

# Example usage
if __name__ == "__main__":
    print(suggest_frequency())
