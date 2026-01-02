from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64, smtplib, random, logging
from email.mime.text import MIMEText
from datetime import datetime
import os

# === Flask Setup ===
app = Flask(__name__)
CORS(app)
otp_store = {}

# === Logging Setup ===
LOG_FILE = "C:/Users/HP/Desktop/log_symm.txt"  # ✅ Update path if needed

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# === Email Config ===
SENDER_EMAIL = "hbhasin5555@gmail.com"
SENDER_PASSWORD = "qnwa jjhr snxi mala "  # App-specific password

# === OTP Manager ===
class OTPManager:
    @staticmethod
    def generate():
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_email(to_email, otp):
        msg = MIMEText(f"Your OTP is: {otp}")
        msg["Subject"] = "OTP Verification"
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pg2.html")
def pg2():
    return render_template("pg2.html")


@app.route("/pg3.html")
def pg3():
    return render_template("pg3.html")

# === Send OTP & Encrypt ===
@app.route("/send-otp", methods=["POST"])
def send_otp():
    data = request.get_json()
    email = data.get("email")
    message = data.get("message")
    password = data.get("password")

    if not all([email, message, password]):
        return jsonify({"message": "Missing fields"}), 400

    try:
        # 1. AES Encryption with password as key
        key = password.encode().ljust(32, b'\0')  # Pad password to 32 bytes
        iv = get_random_bytes(16)
        aes_cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_msg = aes_cipher.encrypt(pad(message.encode(), AES.block_size))

        # 2. RSA Encrypt password (AES key)
        rsa_key = RSA.generate(2048)
        public_key = rsa_key.publickey()
        private_key = rsa_key.export_key()
        cipher_rsa = PKCS1_OAEP.new(public_key)
        encrypted_key = cipher_rsa.encrypt(password.encode())

        # 3. Generate OTP and send email
        otp = OTPManager.generate()
        otp_store[email] = otp
        OTPManager.send_email(email, otp)

        # 4. Log details
        log_entry = (
            f"\n--- Encrypted Session ---\n"
            f"Email: {email}\n"
            f"OTP: {otp}\n"
            f"Encrypted Message: {base64.b64encode(encrypted_msg).decode()}\n"
            f"Encrypted AES Key (RSA): {base64.b64encode(encrypted_key).decode()}\n"
            f"IV: {base64.b64encode(iv).decode()}\n"
            f"{'-'*40}\n"
        )
        logging.info(log_entry)

        # 5. Return JSON to frontend
        return jsonify({
            "message": "OTP sent",
            "encrypted_message": base64.b64encode(encrypted_msg).decode(),
            "iv": base64.b64encode(iv).decode(),
            "encrypted_key": base64.b64encode(encrypted_key).decode(),
            "private_key": private_key.decode()
        }), 200

    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500

# === OTP Verification ===
@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    if not all([email, otp]):
        return jsonify({"message": "Missing fields"}), 400

    if otp_store.get(email) == otp:
        return jsonify({"message": "OTP verified"}), 200
    return jsonify({"message": "Invalid OTP"}), 401
@app.route("/log-decryption", methods=["POST"])
def log_decryption():
    data = request.get_json()
    email = data.get("email")
    decrypted_message = data.get("decryptedMessage")

    if not all([email, decrypted_message]):
        return jsonify({"message": "Missing fields"}), 400

    log_entry = (
        f"\n--- Decryption Event ---\n"
        f"Email: {email}\n"
        f"Decrypted Message: {decrypted_message}\n"
        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{'-'*40}\n"
    )
    logging.info(log_entry)
    f"{'-'*40}\n"


    return jsonify({"message": "Decryption logged"}), 200



# === Start Server ===
if __name__ == "__main__":
    logging.info("\n" + "="*60 + "\nServer Started - New Session\n" + "="*60)
    print("Flask is ready to start...")
    print("Visit: https://127.0.0.1:5050/ or http://localhost:5050/")

    app.run(debug=True, port=5050)
    