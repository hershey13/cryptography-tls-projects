from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import os

def encrypt_aes(data, password):
    key = hashlib.sha256(password).digest()
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return iv + encrypted

def decrypt_aes(ciphertext, password):
    key = hashlib.sha256(password).digest()
    iv = ciphertext[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)
    return decrypted
