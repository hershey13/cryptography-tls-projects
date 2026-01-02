import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode

KEY_PATH = 'backend/rsa_key.pem'
PUBLIC_KEY_PATH = 'backend/public_key.pem'

def generate_keys():
    os.makedirs(os.path.dirname(KEY_PATH), exist_ok=True)

    if os.path.exists(KEY_PATH) and os.path.exists(PUBLIC_KEY_PATH):
        return

    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(KEY_PATH, 'wb') as f:
        f.write(private_key)
    with open(PUBLIC_KEY_PATH, 'wb') as f:
        f.write(public_key)

def get_public_key_pem():
    with open(PUBLIC_KEY_PATH, 'rb') as f:
        return f.read().decode()

def decrypt_rsa(encrypted_b64):
    with open(KEY_PATH, 'rb') as f:
        private_key = RSA.import_key(f.read())
    cipher = PKCS1_OAEP.new(private_key)
    decrypted = cipher.decrypt(b64decode(encrypted_b64))
    return decrypted.decode()
