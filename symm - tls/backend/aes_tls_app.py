from flask import Flask, request, jsonify, render_template
import ssl
from flask_cors import CORS
from aes_util import encrypt_message, decrypt_message, roll_password, unroll_password
from email_util import send_email
import os
import logging
import re

# Log to Desktop
log_path = os.path.join(os.path.expanduser("~"), "Desktop", "log_symm_tls.txt")
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.getLogger("").addHandler(console)

app = Flask(__name__)
CORS(app, origins=["https://127.0.0.1:5000"])  #  Allow only this domain

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt_route():
    try:
        data = request.get_json()
        logging.info(f"📥 /encrypt received: {data}")

        email = data.get("email")
        message = data.get("message")
        password = data.get("password")

        if not (email and message and password):
            logging.warning("⚠️ Missing fields")
            return jsonify({"error": "Missing fields"}), 400

        encrypted = encrypt_message(message, password)
        rolled_pwd = roll_password(password)

        logging.info(f"✅ Encrypted for {email}")
        logging.info(f"🔐 Rolled password: {rolled_pwd}")
        logging.info(f"🔐 Cipher preview: {encrypted[:40]}...")

        send_email(email, encrypted, rolled_pwd)

        return jsonify({"ciphertext": encrypted})

    except Exception as e:
        logging.error("❌ Encryption failed", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/decrypt", methods=["POST"])
def decrypt_route():
    try:
        data = request.get_json()
        logging.info(f"📥 /decrypt received: {data}")

        rolled = data.get("password")
        ciphertext = data.get("ciphertext")
        f"{'-'*40}\n"

        if not (ciphertext and rolled):
            return jsonify({"error": "Missing fields"}), 400

        password = unroll_password(rolled)
        decrypted = decrypt_message(ciphertext, password)

        if decrypted is None:
            logging.warning("❌ Decryption failed.")
            return jsonify({"error": "Decryption failed"}), 400

        return jsonify({"message": decrypted})

    except Exception as e:
        logging.error("❌ Decryption error", exc_info=True)
        return jsonify({"error": str(e)}), 500
def parse_log():
    with open("log.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Reverse for latest first
    lines.reverse()
    password, encrypted = "", ""

    for line in lines:
        if "Rolled password:" in line and not password:
            match = re.search(r"Rolled password:\s*(\S+)", line)
            if match:
                password = match.group(1)

        if "Cipher preview:" in line and not encrypted:
            match = re.search(r"Cipher preview:\s*(.+)", line)
            if match:
                encrypted = match.group(1)

        if password and encrypted:
            break

    return encrypted, password

@app.route('/decrypt')
def decrypt():
    encrypted_msg, password = parse_log()
    return render_template("decrypt.html", encrypted_msg=encrypted_msg, password=password)    
# def decrypt_page():
#     # Read the last line from log file (assuming it's the latest log)
   
#     with open(log_path, "r") as f:
#         lines = f.readlines()
    
#     # Extract from last non-empty line
#     for line in reversed(lines):
#         if line.strip():
#             match = re.search(r'Encrypted Message: (.*?)\s*\|\|\|\| Password: (.*?)$', line)
#             if match:
#                 encrypted_msg = match.group(1)
#                 password = match.group(2)
#                 break
#     else:
#         encrypted_msg = ""
#         password = ""

#     # Pass to frontend
#     return render_template("decrypt.html", encrypted_msg=encrypted_msg, password=password)

# @app.route("/decrypt.html")
# def decrypt_page():
#     return render_template("decrypt.html")


@app.route("/.well-known/<path:subpath>")
def well_known(subpath):
        logging.info(f"🔍 Ignoring Chrome DevTools probe: /.well-known/{subpath}")
        return "", 204  # No Content (or 200 if you prefer)
    
      
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cert_path = os.path.join(base_dir, "certs", "server.crt")
    key_path = os.path.join(base_dir, "certs", "server.key")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path)

    logging.info("🚀 Running Flask over HTTPS at https://127.0.0.1:5000")
    app.run(ssl_context=context, host="127.0.0.1", port=5000, debug=True)


