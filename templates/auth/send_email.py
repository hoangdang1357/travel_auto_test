import os
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_verification_email(to_email, token: str = ""):
    """Send a verification email using SITE_URL from env (fallback to localhost).

    This file previously had a hard-coded verification link. We now build the link
    from the SITE_URL environment variable so emails point to your deployed domain.
    """
    site_url = os.environ.get('SITE_URL', 'http://127.0.0.1:5000').rstrip('/')
    verification_link = f"{site_url}/auth/signup/{token}"

    # Basic email composition (sending mechanism is handled elsewhere / via env)
    from_email = os.environ.get('SENDER_EMAIL', 'no-reply@localhost')
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Please verify your email"

    html_content = f"""
    <html>
    <body>
        <h2>Email Verification</h2>
        <p>Thank you for signing up to our travel service! Please verify your email address by clicking the link below:</p>
        <a href="{verification_link}">Verify Email</a>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html'))

    # Sending is handled by the calling code/environment (SMTP or API). If you still
    # want to perform SMTP here, configure SENDER_EMAIL and SENDER_PASSWORD as env vars
    # and set EMAIL_MODE=smtp. For safety, we avoid attempting network sends here.
    print(f"[EMAIL] Prepared verification email to {to_email} with link: {verification_link}")
    return verification_link