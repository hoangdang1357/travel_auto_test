from smtplib import SMTP, SMTP_SSL, SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import ssl

load_dotenv()

def _get_env(name: str, default=None, required: bool = False):
    value = os.getenv(name, default)
    if required and (value is None or value == ""):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def send_verification_email(to_email, token: str = ""):
    """Send an email with a verification link.

    Expected env vars:
    - SMTP_HOST (default: smtp.gmail.com)
    - SMTP_PORT (default: 465)
    - SMTP_USER (required)
    - SMTP_PASS (required)
    - SMTP_USE_SSL (optional: 'true'/'false'; default inferred from port: 465 => SSL, 587 => STARTTLS)
    - SMTP_TIMEOUT (optional seconds, default 15)
    """

    host = _get_env('SMTP_HOST', 'smtp.gmail.com')
    port_str = _get_env('SMTP_PORT', '465')
    try:
        port = int(port_str)
    except ValueError:
        raise RuntimeError(f"Invalid SMTP_PORT value: {port_str!r}. Must be an integer.")

    sender_email = _get_env('SMTP_USER', required=True)
    sender_password = _get_env('SMTP_PASS', required=True)

    verification_link_base = f'http://127.0.0.1:5000/auth/signup/{token}'
    from_email = sender_email

    # Build message
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

    # Connection preferences
    timeout = float(_get_env('SMTP_TIMEOUT', '15'))
    use_ssl_env = os.getenv('SMTP_USE_SSL')
    if use_ssl_env is not None:
        use_ssl = use_ssl_env.strip().lower() in ('1', 'true', 'yes', 'on')
    else:
        # Infer from common ports
        use_ssl = (port == 465)

    context = ssl.create_default_context()

    try:
        if use_ssl:
            # SSL/TLS from the start (e.g., Gmail on 465)
            with SMTP_SSL(host=host, port=port, timeout=timeout, context=context) as server:
                server.login(sender_email, sender_password)
                server.sendmail(from_email, to_email, msg.as_string())
        else:
            # Plain connection upgraded to TLS (e.g., port 587)
            with SMTP(host=host, port=port, timeout=timeout) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(sender_email, sender_password)
                server.sendmail(from_email, to_email, msg.as_string())
        print(f"Verification email sent to {to_email} via {host}:{port} (SSL={use_ssl})")
        return True
    except (SMTPException, OSError, ssl.SSLError) as e:
        # Log the error for diagnostics. In production, prefer proper logging.
        print(f"Failed to send verification email to {to_email} via {host}:{port} (SSL={use_ssl}): {e}")
        return False
        
