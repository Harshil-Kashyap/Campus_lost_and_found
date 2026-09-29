import hashlib
from db import get_db


def make_pwd(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()


def login(email, pwd):
    db = get_db()
    row = db.execute('SELECT * FROM users WHERE email=? AND pwd=?',
                     (email.lower().strip(), make_pwd(pwd))).fetchone()
    db.close()
    return row


def register(name, email, pwd):
    name = name.strip()
    email = email.lower().strip()
    if not name or not email or not pwd:
        return False, 'All fields are required.'
    if '@' not in email:
        return False, 'Enter a valid email.'
    db = get_db()
    try:
        db.execute('INSERT INTO users(name,email,pwd) VALUES(?,?,?)',
                   (name, email, make_pwd(pwd)))
        db.commit()
        return True, 'Account created.'
    except Exception:
        return False, 'Email is already registered.'
    finally:
        db.close()
