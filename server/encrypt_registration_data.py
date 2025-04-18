import os
import django
import environ
import json
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Util.Padding import pad

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join('backend', '.env'))

PAYLOAD_SECRET = env('PAYLOAD_SECRET')

def to_bytes(data):
    if isinstance(data, str):
        return data.encode('utf-8')
    return data

def bytes_to_key(password, salt, key_length):
    return PBKDF2(password, salt, dkLen=key_length, count=1000)

def encrypt(message, passphrase):
    message = to_bytes(message)
    passphrase = to_bytes(passphrase)
    salt = os.urandom(8)
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(message, AES.block_size))).decode('utf-8')

# Registration data
registration_data = {
  "email": "amaniitjeeaspirant@gmail.com",
  "username": "aman1808",
  "first_name": "Aman",
  "last_name": "Mishra",
  "avatar_idx": 2,
  "institution": "NIT Agartala",
  "phone_no": "9832776728",
  "password": "securepassword123",
  "confirm_password": "securepassword123"
}

# Convert to JSON string
json_data = json.dumps(registration_data)

# Encrypt the data
encrypted_data = encrypt(json_data, PAYLOAD_SECRET)

print("=== ENCRYPTED REGISTRATION DATA ===")
print(encrypted_data)
print("\n=== INSTRUCTIONS ===")
print("1. Copy the encrypted data above")
print("2. In Postman:")
print("   - Set the URL to: http://AMAN_LAPTOP:8000/api/auth/register")
print("   - Set the method to: POST")
print("   - Set the Content-Type header to: text/plain")
print("   - Paste the encrypted data in the request body")
print("   - Send the request")
