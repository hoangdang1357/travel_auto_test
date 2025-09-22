from smtplib import SMTP, SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
<<<<<<< HEAD
from dotenv import load_dotenv
import os

load_dotenv()

def send_verification_email(to_email, token = ""):
    sender_email = os.getenv('SMTP_USER')
    sender_password = os.getenv('SMTP_PASS')
=======



def send_verification_email(to_email, token = ""):
    sender_email = 'dangbaohoang1368@gmail.com'
    sender_password = 'crqbekuljoogyjgo'
>>>>>>> 1f58bd4957a6ed3a7d95c8be6cb16bb83b883c07
    verification_link_base = f'https://hoang.pythonanywhere.com/auth/signup/{token}'
    from_email = sender_email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Please verify your email"
    
    html_content = f"""
    <html>
    <body>
        <h2>Email Verification</h2>
        <p>Thank you for signing up to our travel service! Please verify your email address by clicking the link below:</p>
        <a href="{verification_link_base}">Verify Email</a>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html'))

<<<<<<< HEAD
    with SMTP_SSL(os.getenv('SMTP_HOST'), os.getenv('SMTP_PORT')) as server:
=======
    with SMTP_SSL('smtp.gmail.com', 465) as server:
>>>>>>> 1f58bd4957a6ed3a7d95c8be6cb16bb83b883c07
        server.login(sender_email, sender_password)
        server.sendmail(from_email, to_email, msg.as_string())
        print(f"Verification email sent to {to_email}")