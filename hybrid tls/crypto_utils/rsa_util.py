from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def encrypt_rsa(data, pub_key_bytes):
    pub_key = RSA.import_key(pub_key_bytes)
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(data)

def decrypt_rsa(ciphertext, priv_key_bytes):
    priv_key = RSA.import_key(priv_key_bytes)
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)
