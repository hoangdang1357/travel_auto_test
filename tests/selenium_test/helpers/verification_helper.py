import os
import sqlite3
from typing import Optional
import requests
import json

DB_PATH = os.getenv('TEST_DB_PATH', os.path.join(os.getcwd(), 'travel.db'))
# Default to the deployed site host used by your tests. Can be overridden with TEST_APP_HOST env var.
APP_HOST = os.getenv('TEST_APP_HOST', 'https://hoang.pythonanywhere.com')

def get_verification_url_for_email(email: str) -> Optional[str]:
    """Return the verification URL for the latest verification_code for `email` if present.

    NOTE: This helper reads a local SQLite DB file (default: travel.db) and returns a URL
    using APP_HOST (default: https://hoang.pythonanywhere.com). If you registered against
    the deployed site (hosted on hoang.pythonanywhere.com), the verification token will be
    stored in the remote DB on the deployed server, not in the local `travel.db`. In that case
    this helper won't find a token locally and will return None.

    Options if testing the deployed site:
    - Configure the deployed app to send emails to a test SMTP/mail-capture (Mailtrap, MailHog)
      and read the verification link from that service's API.
    - If you can provide access to the deployed database (or copy it locally), this helper
      can query for the token.
    - Fallback: let the test use the Gmail UI flow (less reliable).
    """
    # First try local DB lookup (useful when testing a local instance)
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT verification_code FROM customers WHERE email = ? ORDER BY customer_id DESC LIMIT 1', (email,))
        row = cur.fetchone()
        conn.close()
        if row and row['verification_code']:
            token = row['verification_code']
            return f"{APP_HOST}/auth/signup/{token}"

    # If local lookup failed and APP_HOST is remote, try the test-only HTTP endpoint
    try:
        endpoint = f"{APP_HOST}/auth/_test/get_verification_token"
        # The test key should be provided via TEST_ENDPOINT_KEY env var
        test_key = os.getenv('TEST_ENDPOINT_KEY', '')
        if not test_key:
            return None
        resp = requests.post(endpoint, json={'email': email, 'key': test_key}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            token = data.get('token')
            if token:
                return f"{APP_HOST}/auth/signup/{token}"
    except Exception:
        # ignore network errors here; return None to allow fallback
        return None
    return None
