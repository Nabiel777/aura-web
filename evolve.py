import os
import json
from datetime import datetime
from collections import Counter

# Directory where learned knowledge is stored
KNOWLEDGE_DIR = "knowledge"
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

# Log file for tracking usage
ACTION_LOG_FILE = "aura_actions.json"

def log_action(command, response):
    """Log every interaction for future improvement"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "response": response
    }

    if not os.path.exists(ACTION_LOG_FILE):
        with open(ACTION_LOG_FILE, "w") as f:
            json.dump([], f)

    with open(ACTION_LOG_FILE, "r") as f:
        logs = json.load(f)

    logs.append(entry)

    with open(ACTION_LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


def get_trend():
    """Get most used command types"""
    if not os.path.exists(ACTION_LOG_FILE):
        return "No trend yet."

    with open(ACTION_LOG_FILE, "r") as f:
        logs = json.load(f)

    commands = [log["command"].split()[0] for log in logs if log["command"]]
    counter = Counter(commands)
    most_common = counter.most_common(1)

    return most_common[0][0] if most_common else "No trend"


def evolve_suggestion():
    """Suggest next area to improve"""
    trend = get_trend()

    suggestions = {
        "learn": "Consider adding real-time web search support.",
        "query": "You should expand local knowledge storage and indexing.",
        "echo": "Try implementing a chat memory module.",
        "greet": "Personalize greetings based on user ID or history",
        "time": "Add timezone-aware time handling",
        "status": "Implement health checks and auto-recovery"
    }

    return suggestions.get(trend, "Unknown trend. Consider improving general knowledge access.")


def save_knowledge(topic, content):
    """Save learned knowledge locally"""
    with open(f"{KNOWLEDGE_DIR}/{topic}.txt", "w", encoding="utf-8") as f:
        f.write(content)