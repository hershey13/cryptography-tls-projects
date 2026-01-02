from flask import Flask, request, jsonify, render_template
from rsa_utils import generate_keys, get_public_key_pem, decrypt_rsa
import ssl
import os
import logging
import os
import smtplib
from email.mime.text import MIMEText

def send_email(to_address, encrypted_msg):
    sender = "hbhasin5555@gmail.com"
    password = "qnwa jjhr snxi mala"

    msg = MIMEText(f" Your encrypted message:\n\n{encrypted_msg}")
    msg["Subject"] = "Your Encrypted Message"
    msg["From"] = sender
    msg["To"] = to_address

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

# Set log path to Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
log_file = os.path.join(desktop_path, "asymm_tls_log.txt")

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

app = Flask(__name__)

# 🔐 Generate RSA keys on startup
generate_keys()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/decrypt')
def decrypt_page():
    return render_template('decrypt.html')

@app.route('/get-public-key')
def get_public_key():
    return jsonify({'public_key': get_public_key_pem()})

@app.route('/submit', methods=['POST'])
def submit_encrypted():
    data = request.json
    encrypted_message = data.get('encrypted_message')
    email = data.get('email')

    logging.info(f" Encrypted message received for {email}")

    # Send email
    try:
        send_email(email, encrypted_message)
        logging.info(f" Encrypted message emailed to {email}")
    except Exception as e:
        logging.error(f"Email failed: {str(e)}")

    return jsonify({'status': 'received', 'data': encrypted_message})


@app.route('/decrypt-message', methods=['POST'])
def decrypt_message():
    data = request.json
    encrypted = data.get('encrypted_message')
    try:
        decrypted = decrypt_rsa(encrypted)
        logging.info(f"Message decrypted: {decrypted}")
        
        return jsonify({'decrypted': decrypted})
        logging.info("-" * 80)
        
    except Exception as e:
        logging.error(f" Decryption error: {str(e)}")
        
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    cert_path = os.path.join(base_dir, 'cert.pem')
    key_path = os.path.join(base_dir, 'key.pem')

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path)

    print(" Flask app running securely at: https://127.0.0.1:5443/")
    app.run(host='127.0.0.1', port=5443, ssl_context=context)
