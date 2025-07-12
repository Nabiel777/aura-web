from cryptography.fernet import Fernet

key = Fernet.generate_key()
print("🔒 Your Encryption Key:")
print(key.decode())