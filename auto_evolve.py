import os
import json
from datetime import datetime
from evolve import log_action, get_trend, evolve_suggestion, save_knowledge
from cryptography.fernet import Fernet

# 🔐 Use the same encryption key as server
ENCRYPTION_KEY = b"aBwnzjV2tf8UyRboLQODQHpuOl9PwvAIDZ4ujDxVMgE="
fernet = Fernet(ENCRYPTION_KEY)

# Knowledge base setup
KNOWLEDGE_DIR = "knowledge"
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

def load_evolved_behaviors():
    """Load previously evolved behaviors"""
    if not os.path.exists("evolved_behaviors.json"):
        with open("evolved_behaviors.json", "w") as f:
            json.dump([], f)

    with open("evolved_behaviors.json", "r") as f:
        return json.load(f)

def save_evolved_behavior(name, behavior):
    """Save evolved behavior to file"""
    behaviors = load_evolved_behaviors()
    behaviors.append({
        "timestamp": datetime.now().isoformat(),
        "behavior_name": name,
        "behavior_code": behavior
    })

    with open("evolved_behaviors.json", "w") as f:
        json.dump(behaviors, f, indent=2)


def suggest_new_command():
    """Suggest new command based on trend"""
    trend = get_trend()

    suggestions = {
        "learn": ("search", "Add web search support"),
        "query": ("index", "Improve local knowledge indexing"),
        "echo": ("chat", "Add memory-based chat enhancements"),
        "greet": ("personalize", "Personalize greetings using user ID"),
        "time": ("timezone", "Add timezone-aware time handling")
    }

    return suggestions.get(trend, ("none", "No evolution needed at this time."))


def auto_add_search_support():
    """Generate code for new 'search' command"""
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


def auto_evolve():
    """Run daily evolution process"""
    print("🧬 Starting Auto-Evolution Module")

    # Load current app logic
    try:
        with open("aura_portal.py", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError as e:
        print(f"❌ Failed to read aura_portal.py: {e}")
        return

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

    # Find insertion point
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
    with open("aura_portal.py", "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Log action
    log_action(f"Auto-added command: {name}", f"Suggestion: {suggestion}")
    save_evolved_behavior(name, new_code)

    print(f"🧩 Evolved! Added new command: {name}")
    print(f"💡 Suggestion: {suggestion}")


if __name__ == "__main__":
    auto_evolve()