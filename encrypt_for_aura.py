from cryptography.fernet import Fernet

# Replace with your real key
ENCRYPTION_KEY = "aBwnzjV2tf8UyRboLQODQHpuOl9PwvAIDZ4ujDxVMgE="
fernet = Fernet(ENCRYPTION_KEY.encode())

cmd = "time"
encrypted_cmd = fernet.encrypt(cmd.encode()).decode()

print("🔐 Encrypted command:")
print(encrypted_cmd)