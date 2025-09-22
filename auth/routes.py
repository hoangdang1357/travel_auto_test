from werkzeug.security import generate_password_hash, check_password_hash

# Giả sử ta dùng dictionary giả lập database
users_db = {}


def signup(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return False, "Email and password required"

    if email in users_db:
        return False, "User already exists"

    hashed = generate_password_hash(password)
    users_db[email] = hashed
    return True, "Signup ok"


def signin(data):
    email = data.get("email")
    password = data.get("password")

    if email not in users_db:
        return False, "user not found"

    if check_password_hash(users_db[email], password):
        return True, "Signin ok"
    else:
        return False, "wrong password"
