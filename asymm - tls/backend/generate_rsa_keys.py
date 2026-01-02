from Crypto.PublicKey import RSA
import os

private_key_path = 'backend/rsa_key.pem'
public_key_path = 'backend/public_key.pem'

os.makedirs('backend', exist_ok=True)

key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

with open(private_key_path, 'wb') as f:
    f.write(private_key)

with open(public_key_path, 'wb') as f:
    f.write(public_key)

print("✅ RSA key pair generated!")
