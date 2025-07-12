
from flask import Flask, request, jsonify
import json
import datetime
from cryptography.fernet import Fernet

app = Flask(__name__, static_folder='.')

# Load directive
with open("aura_directive.json", "r") as f:
    directive = json.load(f)

# 🔒 Replace this with your real key from generate_key.py
ENCRYPTION_KEY = b"aBwnzjV2tf8UyRboLQODQHpuOl9PwvAIDZ4ujDxVMgE="  # ← Use your own generated key here
fernet = Fernet(ENCRYPTION_KEY)

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
                "error": "No command received",
                "received_data": data
            }), 400

        # 🔐 Decrypt incoming command
        decrypted_bytes = fernet.decrypt(encrypted_cmd.encode())
        cmd = decrypted_bytes.decode().lower()

        # 🧠 Process command
        if cmd == "status":
            response = "Status: Online"
        elif cmd == "time":
            response = f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elif cmd == "greet":
            response = "Hello, Creator."
        elif cmd.startswith("echo "):
            response = f"You said: {cmd[5:]}"
        else:
            response = f"Unknown command: '{cmd}'"

        # 🔒 Encrypt outgoing response
        encrypted_response = fernet.encrypt(response.encode()).decode()
        return jsonify({"response": encrypted_response})

    except Exception as e:
        return jsonify({
            "error": "Decryption or processing failed",
            "details": str(e),
            "raw_received_command": encrypted_cmd,
            "key_used": ENCRYPTION_KEY.decode(),
            "type_of_error": type(e).__name__
        }), 400

@app.route("/aura_ui_simple.html")
def simple_ui():
    return app.send_static_file("aura_ui_simple.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)