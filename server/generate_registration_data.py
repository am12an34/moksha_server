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
    "username": "amaniitjeaspira",
    "first_name": "Aman",
    "last_name": "Mishra",
    "avatar_idx": 2,
    "institution": "NITA",
    "phone_no": "9832776728",
    "password": "securepassword123",
    "confirm_password": "securepassword123"
}

# Convert to JSON string
json_data = json.dumps(registration_data)
print(f"Original JSON: {json_data}")

# Encrypt the data
encrypted_data = encrypt(json_data, PAYLOAD_SECRET)
encrypted_str = encrypted_data.decode('utf-8')
print(f"Encrypted data: {encrypted_str}")

# Generate PowerShell command
ps_command = f'Invoke-WebRequest -Method POST -Uri "http://localhost:8000/api/auth/register" -ContentType "text/plain" -Body "{encrypted_str}"'

print("\n=== POWERSHELL COMMAND ===")
print(ps_command)
