from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_verification_email(to_email, token=""):
    sender_email = os.getenv("SMTP_USER", "dangbaohoang1368@gmail.com")
    sender_password = os.getenv("SMTP_PASS", "crqbekuljoogyjgo")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 465))

    verification_link_base = f"https://hoang.pythonanywhere.com/auth/signup/{token}"

    # Tạo nội dung email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = "Please verify your email"

    html_content = f"""
    <html>
    <body>
        <h2>Email Verification</h2>
        <p>Thank you for signing up to our travel service! Please verify your email address by clicking the link below:</p>
        <a href="{verification_link_base}">Verify Email</a>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    # Gửi email
    with SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        print(f"Verification email sent to {to_email}")
