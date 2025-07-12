import os
import json
from datetime import datetime

# Knowledge storage directory
KNOWLEDGE_DIR = "knowledge"
if not os.path.exists(KNOWLEDGE_DIR):
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

# Action log file
ACTION_LOG_FILE = "aura_actions.json"

def log_action(command, response):
    ...
    """Log every interaction for trend tracking"""
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
    """Identify most used command types"""
    if not os.path.exists(ACTION_LOG_FILE):
        return "No trend yet."

    with open(ACTION_LOG_FILE, "r") as f:
        logs = json.load(f)

    from collections import Counter
    trends = [log["command"].split()[0] for log in logs]
    most_common = Counter(trends).most_common(1)

    return most_common[0][0] if most_common else "No trend"


def evolve_suggestion():
    """Return a suggested improvement based on usage"""
    trend = get_trend()

    suggestions = {
        "learn": "Add real-time web search support.",
        "query": "Expand local knowledge indexing system.",
        "echo": "Build memory-based chat enhancements.",
        "greet": "Personalize greetings using user ID.",
        "time": "Add timezone-aware time handling.",
        "status": "Implement health checks and auto-recovery."
    }

    return suggestions.get(trend, "Unknown trend. Consider improving general knowledge access.")


def save_knowledge(topic, content):
    """Save learned knowledge locally"""
    with open(f"{KNOWLEDGE_DIR}/{topic}.txt", "w", encoding="utf-8") as f:
        f.write(content)