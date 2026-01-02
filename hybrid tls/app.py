from flask import Flask, render_template, request
from crypto_utils.aes_util import encrypt_aes, decrypt_aes
from crypto_utils.rsa_util import encrypt_rsa, decrypt_rsa
from base64 import b64encode, b64decode
import os

app = Flask(__name__)

# Load RSA public and private keys
with open("public_key.pem", "rb") as f:
    public_key = f.read()

with open("private_key.pem", "rb") as f:
    private_key = f.read()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    message = request.form["message"]
    email = request.form["email"]
    password = request.form["password"].encode()

    # AES encrypt the message
    aes_encrypted = encrypt_aes(message.encode(), password)

    # Encrypt the AES key with RSA
    encrypted_key = encrypt_rsa(password, public_key)

    # Combine and Base64 encode the result
    full_payload = b64encode(encrypted_key + b"||" + aes_encrypted).decode()

    # (Optional) Log for debugging
    print(f"[+] Encrypted message for {email}: {full_payload[:60]}...")

    return f"<h3>Encrypted Message:</h3><pre>{full_payload}</pre><a href='/'>Go back</a>"

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    if request.method == "POST":
        try:
            encrypted_message = request.form["encrypted_message"]
            password_input = request.form["password"].encode()

            # Decode base64 and split
            full_payload = b64decode(encrypted_message)
            encrypted_key, aes_cipher = full_payload.split(b"||", 1)

            # RSA decrypt AES key
            aes_key = decrypt_rsa(encrypted_key, private_key)

            # Validate user-provided password matches decrypted key
            if aes_key != password_input:
                return render_template("decrypt.html", decrypted_message="Invalid password or mismatched key.")

            # AES decrypt the message
            decrypted = decrypt_aes(aes_cipher, aes_key).decode()

            return render_template("decrypt.html", decrypted_message=decrypted)
        except Exception as e:
            return render_template("decrypt.html", decrypted_message=f"Decryption failed: {str(e)}")
    
    return render_template("decrypt.html")

if __name__ == "__main__":
    # Use TLS cert and key (self-signed)
    app.run(ssl_context=("cert.pem", "key.pem"), debug=True)
