import os
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_verification_email(to_email: str, token: str = "") -> bool:
    """Send a verification email.

    Uses environment variables for configuration. If EMAIL_MODE=console or SMTP credentials
    are missing/unusable, it will print the verification link to stdout and return False,
    but it will not raise, so the app flow can continue.

    Env vars:
      - EMAIL_MODE: 'smtp' (default) or 'console'
      - SMTP_HOST: default 'smtp.gmail.com'
      - SMTP_PORT: default '465'
      - SENDER_EMAIL, SENDER_PASSWORD: required for SMTP mode
      - SITE_URL: base site URL, default 'http://127.0.0.1:5000'
    """

    site_url = os.environ.get('SITE_URL', 'http://127.0.0.1:5000')
    verification_link = f"{site_url}/auth/signup/{token}"

    mode = os.environ.get('EMAIL_MODE', 'smtp').lower()
    if mode == 'console':
        print(f"[EMAIL CONSOLE MODE] To: {to_email} — Verify at: {verification_link}")
        return False

    host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    port = int(os.environ.get('SMTP_PORT', '465'))
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')

    if not sender_email or not sender_password:
        print("[EMAIL] Missing SMTP credentials. Falling back to console output.")
        print(f"[EMAIL FALLBACK] To: {to_email} — Verify at: {verification_link}")
        return False

    msg = MIMEMultipart()
    msg['From'] = sender_email
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

    try:
        with SMTP_SSL(host, port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"Verification email sent to {to_email}")
            return True
    except Exception as e:
        # Network may be restricted on the host (e.g., Render blocks outbound SMTP).
        print(f"[EMAIL ERROR] {e}. Falling back to console output.")
        print(f"[EMAIL FALLBACK] To: {to_email} — Verify at: {verification_link}")
        return False