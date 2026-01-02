from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import base64

# Derive 256-bit AES key from password using SHA-256
def get_aes_key(password: str) -> bytes:
    return sha256(password.encode()).digest()

# AES encryption
def encrypt_message(message: str, password: str) -> str:
    key = get_aes_key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode()
    ct = base64.b64encode(ct_bytes).decode()
    return f"{iv}:{ct}"


# AES decryption
def decrypt_message(ciphertext: str, password: str) -> str:
    try:
        iv, ct = ciphertext.split(":")
        key = get_aes_key(password)
        iv = base64.b64decode(iv)
        ct = base64.b64decode(ct)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode()
    except Exception:
        return None

# Caesar shift (+2)
def roll_password(password: str) -> str:
    return ''.join(chr((ord(c) + 2) % 256) for c in password)

# Caesar unshift (-2)
def unroll_password(rolled: str) -> str:
    return ''.join(chr((ord(c) - 2) % 256) for c in rolled)
