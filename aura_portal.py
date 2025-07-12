from flask import Flask, request, jsonify
import json
import datetime
from cryptography.fernet import Fernet
import os

app = Flask(__name__, static_folder='.')

# 🔒 Use your fixed key
ENCRYPTION_KEY = b"aBwnzjV2tf8UyRboLQODQHpuOl9PwvAIDZ4ujDxVMgE="
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
                "error": "Missing command",
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
            "error": "Invalid or missing command",
            "details": str(e),
            "raw_command": encrypted_cmd,
            "key_used": ENCRYPTION_KEY.decode(),
            "type_of_error": type(e).__name__
        }), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)