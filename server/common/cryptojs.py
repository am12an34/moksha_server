from Cryptodome import Random
from Cryptodome.Cipher import AES
from hashlib import md5
import base64

BLOCK_SIZE = 16


def pad(data: bytes) -> bytes:
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length)*length).encode()


def unpad(data) -> bytes:
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]


def to_bytes(str_or_bytes: str | bytes) -> bytes:
    if type(str_or_bytes) is bytes:
        return str_or_bytes
    elif type(str_or_bytes) is str:
        return str_or_bytes.encode()
    else:
        raise TypeError("Expected bytes or string, but got %s." % type(str_or_bytes))


def bytes_to_key(data: bytes, salt: bytes, output=48) -> bytes:
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]


def encrypt(message: str | bytes, passphrase: str | bytes) -> bytes:
    message = to_bytes(message)
    passphrase = to_bytes(passphrase)

    salt = Random.new().read(8)
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(message)))


def decrypt(encrypted: str | bytes, passphrase: str | bytes) -> bytes:
    try:
        # Convert to bytes and decode base64
        encrypted = base64.b64decode(to_bytes(encrypted))
        passphrase = to_bytes(passphrase)

        # Verify the format
        if len(encrypted) < 16 or encrypted[0:8] != b"Salted__":
            raise ValueError("Invalid encrypted data format")

        salt = encrypted[8:16]
        key_iv = bytes_to_key(passphrase, salt, 32+16)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt and unpad
        decrypted = aes.decrypt(encrypted[16:])
        return unpad(decrypted)
    except Exception as e:
        print(f"Decryption error: {str(e)}")
        raise
