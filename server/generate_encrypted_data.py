import os
import django
import environ
import json
from common.cryptojs import encrypt

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join('backend', '.env'))

PAYLOAD_SECRET = env('PAYLOAD_SECRET')

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
print(encrypted_data.decode('utf-8'))
print("\n=== INSTRUCTIONS ===")
print("1. Copy the encrypted data above")
print("2. In Postman:")
print("   - Set the URL to: http://localhost:8000/api/auth/register")
print("   - Set the method to: POST")
print("   - Set the Content-Type header to: text/plain")
print("   - Paste the encrypted data in the request body")
print("   - Send the request")
