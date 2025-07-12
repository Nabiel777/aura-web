import os
import json
from datetime import datetime
from evolve import log_action, get_trend, evolve_suggestion, save_knowledge
from cryptography.fernet import Fernet

# 🔐 Use the same encryption key as server
ENCRYPTION_KEY = b"aBwnzjV2tf8UyRboLQODQHpuOl9PwvAIDZ4ujDxVMgE="
fernet = Fernet(ENCRYPTION_KEY)

# File where evolved behaviors are stored
EVOLVED_BEHAVIORS_FILE = "evolved_behaviors.json"

def load_evolved_behaviors():
    """Load previously evolved behaviors"""
    if not os.path.exists(EVOLVED_BEHAVIORS_FILE):
        return {}
    with open(EVOLVED_BEHAVIORS_FILE, "r") as f:
        return json.load(f)

def save_evolved_behavior(name, behavior):
    """Save a new evolved behavior"""
    behaviors = load_evolved_behaviors()
    behaviors[name] = {
        "behavior": behavior,
        "timestamp": datetime.now().isoformat()
    }
    with open(EVOLVED_BEHAVIORS_FILE, "w") as f:
        json.dump(behaviors, f, indent=2)

def suggest_new_command():
    """Suggest a new command based on trend"""
    trend = get_trend()

    # Map trends to potential new commands
    suggestions = {
        "learn": ("search", "Add web search support to learn from more sources"),
        "query": ("index", "Improve local knowledge indexing"),
        "echo": ("chat", "Add memory-based chat enhancements"),
        "greet": ("personalize", "Personalize greetings using user ID"),
        "time": ("timezone", "Add timezone-aware time handling"),
        "status": ("healthcheck", "Implement health checks and auto-recovery")
    }

    return suggestions.get(trend, ("none", "No immediate suggestion"))


def auto_add_search_support():
    """Auto-generate a 'search' command"""
    return """
elif cmd.startswith("search "):
    topic = cmd[7:]
    try:
        from duckduckgo_search import DDGS
        results = list(DDGS().text(topic, max_results=3))
        summary = "\\n".join([f"- {r['title']}\\n{r['body']}" for r in results])
        response = f"🔍 Search results for '{topic}':\\n{summary}"
    except Exception as e:
        response = f"Search failed: {str(e)}"
"""


def auto_update_directive():
    """Update the directive file with latest evolution goals"""
    with open("aura_directive.json", "r") as f:
        directive = json.load(f)

    # 🧬 Simulate directive improvement
    directive["version"] = "v0.0.2"
    directive["timestamp"] = datetime.now().isoformat()
    directive["evolution_log"] = directive.get("evolution_log", []) + [
        {
            "date": datetime.now().isoformat(),
            "suggestion": suggest_new_command()[1]
        }
    ]

    with open("aura_directive.json", "w") as f:
        json.dump(directive, f, indent=2)


def auto_evolve():
    """Run daily evolution process"""
    print("🧬 Starting Auto-Evolution Module")

    # Get current app logic
    with open("aura_portal.py", "r") as f:
        lines = f.readlines()

    # Find where `/command` route starts
    command_start = None
    for i, line in enumerate(lines):
        if "@app.route(\"/command\"" in line:
            command_start = i
            break

    if command_start is None:
        print("❌ Could not find /command route")
        return

    # Suggest new command
    name, suggestion = suggest_new_command()
    if name == "none":
        print("🧠 No evolution needed at this time.")
        return

    # Generate new code block
    if name == "search":
        new_code = auto_add_search_support()
    else:
        print(f"⚠️ Unknown suggestion: {name}")
        return

    # Insert new command logic
    insert_index = None
    for i, line in enumerate(lines[command_start:], start=command_start):
        if "response = \"Unknown command." in line:
            insert_index = i
            break

    if insert_index is None:
        print("❌ Could not find insertion point")
        return

    # Insert new command logic
    lines.insert(insert_index, new_code)

    # Save updated file
    with open("aura_portal.py", "w") as f:
        f.writelines(lines)

    # Log action
    log_action(f"Auto-added command: {name}", f"Suggestion: {suggestion}")

    print(f"🧩 Evolved! Added new command: {name}")


if __name__ == "__main__":
    auto_evolve()