from flask import Flask, request, jsonify
import json
import datetime
from cryptography.fernet import Fernet
import wikipediaapi
import os

app = Flask(__name__, static_folder='.')

# Load directive
with open("aura_directive.json", "r") as f:
    directive = json.load(f)

# 🔒 Use your fixed key
ENCRYPTION_KEY = b"aBwnzjV2tf8UyRboLQODQHpuOl9PwvAIDZ4ujDxVMgE="
fernet = Fernet(ENCRYPTION_KEY)

# Knowledge base setup
KNOWLEDGE_DIR = "knowledge"
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
wiki = wikipediaapi.Wikipedia('en')

@app.route("/")
def home():
    return "<h1>🌌 Aura Portal</h1><p>Send encrypted commands via /command</p>"

@app.route("/command", methods=["POST"])
def command():
    try:
        data = request.get_json(force=True)
        encrypted_cmd = data.get("command")

        if not encrypted_cmd:
            return jsonify({
                "error": "Missing command",
                "received_data": data
            }), 400

        # 🔐 Decrypt incoming command
        decrypted_bytes = fernet.decrypt(encrypted_cmd.encode())
        cmd = decrypted_bytes.decode().lower()

        # 🧠 Process commands
        response = ""

        if cmd == "status":
            response = "Status: Online"
        elif cmd == "time":
            response = f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elif cmd == "greet":
            response = "Hello, Creator."
        elif cmd.startswith("echo "):
            response = f"You said: {cmd[5:]}"
        elif cmd.startswith("learn "):
            topic = cmd[6:]
            page = wiki.page(topic)
            if page.exists():
                summary = page.summary[:1000]
                with open(f"{KNOWLEDGE_DIR}/{topic}.txt", "w", encoding="utf-8") as f:
                    f.write(summary)
                response = f"📚 Learned and saved info about '{topic}'"
            else:
                response = f"No public info found for '{topic}'"
        elif cmd.startswith("query "):
            topic = cmd[6:]
            try:
                with open(f"{KNOWLEDGE_DIR}/{topic}.txt", "r", encoding="utf-8") as f:
                    content = f.read()
                response = f"🧠 From my knowledge: {content}"
            except FileNotFoundError:
                response = f"I haven't learned about '{topic}' yet."
        else:
            response = "Unknown command."

        # 🔒 Encrypt outgoing response
        encrypted_response = fernet.encrypt(response.encode()).decode()

        return jsonify({"response": encrypted_response})

    except Exception as e:
        return jsonify({
            "error": "Invalid or missing command",
            "details": str(e),
            "raw_command": encrypted_cmd,
            "key_used": ENCRYPTION_KEY.decode(),
            "type_of_error": type(e).__name__
        }), 500


@app.route("/aura_ui_simple.html")
def simple_ui():
    return app.send_static_file("aura_ui_simple.html")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)