import smtplib
from email.message import EmailMessage
import ssl

# 🔐 Gmail SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL port

SENDER_EMAIL = "hbhasin5555@gmail.com"
SENDER_PASSWORD = "qnwa jjhr snxi mala"  

def send_email(receiver_email, encrypted_message, rolled_password):
    msg = EmailMessage()
    msg["Subject"] = "🔐 Your Encrypted Message"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    body = f"""Hello,

Your message has been encrypted successfully.

 Encrypted Message:
{encrypted_message}

Rolled Password :
{rolled_password}

Paste this encrypted message and your original password into the decryption page.

"""
    msg.set_content(body)

    # Send securely over SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
